import sqlite3
import secrets
import csv
from pathlib import Path

# The exact CSV data you provided
CSV_DATA = """username,password,page_url
instructor,20667,http://localhost:8501/?participant=instructor
maryam,2342,http://localhost:8501/?participant=maryam
reza,3125,http://localhost:8501/?participant=reza
hossien,1425,http://localhost:8501/?participant=hossien
elham,2102,http://localhost:8501/?participant=elham
sara,5247,http://localhost:8501/?participant=sara
mostafa,9854,http://localhost:8501/?participant=mostafa
mohammad,3798,http://localhost:8501/?participant=mohammad
reihaneh,2143,http://localhost:8501/?participant=reihaneh
erfan,7514,http://localhost:8501/?participant=erfan
ashkan,2036,http://localhost:8501/?participant=ashkan
mehrnaz,4528,http://localhost:8501/?participant=mehrnaz
hassan,8632,http://localhost:8501/?participant=hassan
person1,5247,http://localhost:8501/?participant=person1
person2,2415,http://localhost:8501/?participant=person2
person3,2594,http://localhost:8501/?participant=person3
person4,2398,http://localhost:8501/?participant=person4
participant17,MaL8DAWJ21xojF1N,http://localhost:8501/?participant=participant17
participant18,0Ib7atXchchqoZ1m,http://localhost:8501/?participant=participant18
participant19,MrLKaOmVeA8WobqN,http://localhost:8501/?participant=participant19
participant20,ktkYYimH2oaUpuG1,http://localhost:8501/?participant=participant20"""

import storage

def run_import():
    # Parse the text into a list of dicts
    lines = CSV_DATA.strip().split('\n')
    reader = csv.DictReader(lines)
    
    # Write to database
    with storage.connect() as c:
        # Clear existing data so we start fresh with your exact list
        c.execute('DROP TABLE IF EXISTS sessions')
        c.execute('DROP TABLE IF EXISTS drafts')
        c.execute('DROP TABLE IF EXISTS attempts')
        c.execute('DROP TABLE IF EXISTS users')
        
        # Recreate tables
        c.execute('CREATE TABLE users(id TEXT PRIMARY KEY, salt TEXT NOT NULL, hash TEXT NOT NULL, role TEXT NOT NULL)')
        c.execute('CREATE TABLE attempts(id INTEGER PRIMARY KEY, user_id TEXT REFERENCES users(id), task_id INTEGER NOT NULL, prompt TEXT, artifact TEXT, reflection TEXT, quiz INTEGER, automatic TEXT, auto_score REAL, status TEXT DEFAULT "pending", rubric TEXT, feedback TEXT, total REAL, created TEXT, reviewed TEXT)')
        c.execute('CREATE TABLE drafts(user_id TEXT REFERENCES users(id), task_id INTEGER, prompt TEXT, artifact TEXT, reflection TEXT, PRIMARY KEY(user_id,task_id))')
        c.execute('CREATE TABLE sessions(token TEXT PRIMARY KEY,user_id TEXT REFERENCES users(id),created REAL)')
        
        out_rows = []
        for row in reader:
            username = row['username']
            password = row['password']
            
            # The instructor must have the instructor role, everyone else is a participant
            role = 'instructor' if username == 'instructor' else 'participant'
            
            # Create secure hash for the database
            salt = secrets.token_hex(16)
            hash_val = storage.password_hash(password, salt)
            
            # Insert into database
            c.execute('INSERT INTO users VALUES(?,?,?,?)', (username, salt, hash_val, role))
            
            # Fix the page_url to match the username properly (person1 had participant13 in your list)
            page_url = f"http://localhost:8501/?participant={username}"
            out_rows.append({'username': username, 'password': password, 'page_url': page_url})
            
    # Save a CSV file on your local machine for your reference
    cred_path = storage.DB.parent / 'credentials.csv'
    cred_path.parent.mkdir(exist_ok=True)
    with open(cred_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['username', 'password', 'page_url'])
        writer.writeheader()
        writer.writerows(out_rows)
        
    print(f"Successfully imported {len(out_rows)} users into {storage.DB}")
    print(f"Updated credentials saved to {cred_path}")

if __name__ == '__main__':
    run_import()
