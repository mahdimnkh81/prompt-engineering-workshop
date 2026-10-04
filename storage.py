"""SQLite persistence and server-side authorization for the workshop."""
import csv
import hashlib
import hmac
import io
import json
import os
from pathlib import Path
import secrets
import sqlite3
from datetime import datetime, timezone
from curriculum import TASKS, PASS_SCORE

ROOT=Path(__file__).resolve().parent
DB=Path(os.environ.get('WORKSHOP_DB', ROOT/'data/workshop.sqlite3'))

def connect():
    DB.parent.mkdir(parents=True,exist_ok=True)
    c=sqlite3.connect(DB, timeout=20)
    c.row_factory=sqlite3.Row
    c.execute('PRAGMA foreign_keys=ON')
    return c

def password_hash(password,salt):
    return hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),180000).hex()

def initialize(base_url='http://localhost:8501'):
    with connect() as c:
        c.execute('PRAGMA journal_mode=WAL')
        c.executescript('''
        CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, salt TEXT NOT NULL, hash TEXT NOT NULL, role TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS attempts(id INTEGER PRIMARY KEY, user_id TEXT REFERENCES users(id), task_id INTEGER NOT NULL, prompt TEXT, artifact TEXT, reflection TEXT, quiz INTEGER, automatic TEXT, auto_score REAL, status TEXT DEFAULT 'pending', rubric TEXT, feedback TEXT, total REAL, created TEXT, reviewed TEXT);
        CREATE TABLE IF NOT EXISTS drafts(user_id TEXT REFERENCES users(id), task_id INTEGER, prompt TEXT, artifact TEXT, reflection TEXT, PRIMARY KEY(user_id,task_id));
        CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY,user_id TEXT REFERENCES users(id),created REAL);
        ''')
        if c.execute('SELECT count(*) FROM users').fetchone()[0]: return False
        rows=[]
        for username in ['instructor']+[f'participant{i:02}' for i in range(1,21)]:
            password=secrets.token_urlsafe(12); salt=secrets.token_hex(16)
            c.execute('INSERT INTO users VALUES(?,?,?,?)',(username,salt,password_hash(password,salt),'instructor' if username=='instructor' else 'participant'))
            rows.append([username,password,base_url.rstrip('/')+'/?participant='+username])
        path=DB.parent/'credentials.csv'
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as f:
            writer=csv.writer(f);writer.writerow(['username','password','page_url']);writer.writerows(rows)
    return True

def login(username,password):
    import time
    with connect() as c:
        row=c.execute('SELECT * FROM users WHERE id=?',(username,)).fetchone()
        # Perform a hash even for unknown names to reduce trivial timing differences.
        digest=password_hash(password,row['salt'] if row else '00'*16)
        if row and hmac.compare_digest(digest,row['hash']):
            token=secrets.token_urlsafe(32)
            c.execute('INSERT INTO sessions VALUES(?,?,?)',(token,username,time.time()))
            return token
    return None

def identity(token):
    import time
    with connect() as c:
        row=c.execute('SELECT u.id,u.role FROM sessions s JOIN users u ON s.user_id=u.id WHERE s.token=? AND s.created>?',(token,time.time()-12*3600)).fetchone()
    if not row: raise PermissionError('Please sign in again; sessions last 12 hours.')
    return dict(row)

def logout(token):
    with connect() as c:c.execute('DELETE FROM sessions WHERE token=?',(token,))

def passed(c,user):
    return {r[0] for r in c.execute("SELECT DISTINCT task_id FROM attempts WHERE user_id=? AND status='passed'",(user,))}

def require_participant(token,task_id,c):
    user=identity(token)
    if user['role']!='participant':raise PermissionError('Participant access required.')
    if task_id not in range(1,len(TASKS)+1):raise ValueError('Unknown task.')
    if not set(range(1,task_id)).issubset(passed(c,user['id'])):raise PermissionError('Pass all earlier tasks first.')
    return user['id']

def attempts(token):
    user=identity(token)
    with connect() as c:
        if user['role']=='instructor':rows=c.execute('SELECT * FROM attempts ORDER BY id DESC').fetchall()
        else:rows=c.execute('SELECT * FROM attempts WHERE user_id=? ORDER BY id DESC',(user['id'],)).fetchall()
    return [dict(r) for r in rows]

def save_draft(token,task_id,prompt,artifact,reflection):
    with connect() as c:
        user=require_participant(token,task_id,c)
        c.execute('INSERT INTO drafts VALUES(?,?,?,?,?) ON CONFLICT(user_id,task_id) DO UPDATE SET prompt=excluded.prompt,artifact=excluded.artifact,reflection=excluded.reflection',(user,task_id,prompt,artifact,reflection))

def get_draft(token,task_id):
    with connect() as c:
        user=require_participant(token,task_id,c)
        r=c.execute('SELECT * FROM drafts WHERE user_id=? AND task_id=?',(user,task_id)).fetchone()
    return dict(r) if r else {}

def roster(token):
    if identity(token)['role']!='instructor':raise PermissionError('Instructor access required.')
    with connect() as c:
        return [{'participant':r[0],'passed':len(passed(c,r[0]))} for r in c.execute("SELECT id FROM users WHERE role='participant' ORDER BY id")]

def export_csv(token):
    if identity(token)['role']!='instructor':raise PermissionError('Instructor access required.')
    rows=attempts(token); out=io.StringIO()
    fields=['id','user_id','task_id','status','auto_score','total','rubric','feedback','prompt','artifact','reflection','created','reviewed','automatic']
    w=csv.DictWriter(out,fieldnames=fields,extrasaction='ignore');w.writeheader()
    for row in rows:
        # Prevent spreadsheet formula execution from participant text.
        w.writerow({k:("'"+v if isinstance(v,str) and v.lstrip().startswith(('=','+','-','@')) else v) for k,v in row.items()})
    return out.getvalue()

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--base-url',default='http://localhost:8501');args=parser.parse_args()
    print('Created 20 participant accounts and instructor.' if initialize(args.base_url) else 'Existing workshop preserved.')
    print('Private credentials file:',DB.parent/'credentials.csv')


def submit_prompt(token,task_id,prompt,quiz=None):
    """Authorize before billing; no database transaction is held over the network."""
    from ai_evaluation import grade_prompt
    if not isinstance(prompt,str) or not 10<=len(prompt.strip())<=20000:
        raise ValueError('Your prompt must contain 10–20,000 characters.')
    with connect() as c:
        user=require_participant(token,task_id,c)
    if type(quiz) is not int or quiz not in range(3):
        raise ValueError('Choose one answer to the concept question before submitting.')
    save_draft(token,task_id,prompt,'','')
    result=grade_prompt(TASKS[task_id-1],prompt)
    # Grading failures throw before insertion: no fabricated zero or accidental pass.
    task=TASKS[task_id-1]
    result['quiz']={'question':task['quiz'],'selected':quiz,'selected_text':task['options'][quiz],'correct':quiz==task['answer']}
    total=result['score']
    now=datetime.now(timezone.utc).isoformat()
    with connect() as c:
        c.execute('BEGIN IMMEDIATE')
        require_participant(token,task_id,c)
        return c.execute('INSERT INTO attempts(user_id,task_id,prompt,artifact,reflection,automatic,auto_score,status,rubric,feedback,total,created,reviewed,quiz) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
            (user,task_id,prompt,'','',json.dumps(result,ensure_ascii=False),total,'passed' if total>=PASS_SCORE and result['quiz']['correct'] else 'revise',json.dumps([r['score'] for r in result['criteria']]),result['summary'],total,now,now,quiz)).lastrowid

def override_attempt_status(token, attempt_id, status):
    if identity(token)['role'] != 'instructor': raise PermissionError('Instructor access required.')
    with connect() as c:
        c.execute('UPDATE attempts SET status=? WHERE id=?', (status, attempt_id))
