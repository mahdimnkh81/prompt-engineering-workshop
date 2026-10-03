import json
import time
from pathlib import Path
import streamlit as st
import storage
from curriculum import TASKS, AGENDA, PASS_SCORE

st.set_page_config(page_title='Prompt Lab · Workshop',page_icon='🧪',layout='wide')
st.markdown('''<style>.stApp {background: #f5f7fb;} h1,h2,h3 {color:#13243b;} div[data-testid="stMetric"] {background:white;padding:16px;border-radius:12px;} .block-container {max-width:1200px;}</style>''',unsafe_allow_html=True)
st.caption('PROMPT LAB  /  THREE-HOUR PRACTICAL WORKSHOP')

if not storage.DB.exists():
    st.error('Initialize the workshop first: python storage.py');st.stop()

if 'token' not in st.session_state:
    st.title('Make your prompts work.')
    st.write('Eight labs. Your own workspace. Feedback before the next challenge.')
    preset=st.query_params.get('participant','')
    with st.form('login'):
        username=st.text_input('Username',value=preset)
        password=st.text_input('Password',type='password')
        clicked=st.form_submit_button('Open my workspace',type='primary')
    if clicked:
        if time.time()<st.session_state.get('login_after',0):st.error('Please wait a moment before trying again.')
        else:
            token=storage.login(username.strip(),password)
            if token:st.session_state.token=token;st.rerun()
            else:st.session_state.login_after=time.time()+2;st.error('Username or password is incorrect.')
    st.info('Use the individual credentials supplied by your instructor. Your page URL does not grant access to another account.')
    st.stop()

try:user=storage.identity(st.session_state.token)
except PermissionError:
    del st.session_state.token;st.rerun()
token=st.session_state.token
with st.sidebar:
    st.title('Prompt Lab')
    st.write(user['id'])
    if st.button('Sign out'):
        storage.logout(token);st.session_state.clear();st.rerun()
    st.caption('AI prompt assessment: four task-specific weighted criteria. Pass with 70/100 and a correct concept answer.')
    with st.expander('Three-hour agenda'):
        for timing,minutes,title in AGENDA:st.write(f'{timing} · {title}')

rows=storage.attempts(token)
if user['role']=='instructor':
    st.title('Instructor dashboard')
    from ai_evaluation import config
    cfg=config()
    st.caption(f"AI evaluator: {cfg['model']} · AvalAI")
    if not cfg['key']:st.warning('Set AVALAI_API_KEY in the server environment or .streamlit/secrets.toml.')
    roster=storage.roster(token); pending=[r for r in rows if r['status']=='pending']
    a,b,c=st.columns(3)
    a.metric('Participants',len(roster));b.metric('Awaiting review',len(pending));c.metric('Completed all labs',sum(r['passed']==8 for r in roster))
    if st.button('Refresh dashboard'):st.rerun()
    progress,answer_tab,history=st.tabs(['Class progress','Instructor answer key','All attempts & export'])
    with answer_tab:
        from instructor_answers import get_answer
        st.subheader('Instructor answer key')
        st.info('These are reference prompts, not the only correct answers or guaranteed AI scores. Accept alternative prompts that meet the rubric. Expected outputs are teaching references; participants submit their prompt and concept answer.')
        answer_id=st.selectbox('Reference lab',range(1,9),format_func=lambda n:f"Lab {n}: {TASKS[n-1]['title']}",key='answer_key_lab')
        reference=get_answer(token,answer_id)
        st.markdown('**Reference submission — paste this into Your prompt**')
        st.caption('This is the instruction the participant should write, not the answer produced by following that instruction.')
        st.code(reference['prompt'],language=None)
        st.markdown('**Why this meets the rubric**')
        st.write(reference['rationale'])
        for criterion in TASKS[answer_id-1]['ai_rubric']:st.write('• '+criterion)
        with st.expander('Teaching illustration only — do not submit this output',expanded=False):
            st.warning('This illustrates what a model might produce after following the reference prompt. Pasting it into Your prompt does not demonstrate prompt-writing skills and may receive a low score.')
            st.code(reference['expected'],language=None)
        st.markdown('**Concept question and correct answer**')
        st.write(reference['question'])
        st.success(f"Option {reference['answer_number']}: {reference['answer']}")
    with progress:
        table=[]
        for member in roster:
            item=dict(member)
            for t in TASKS:
                rs=[r for r in rows if r['user_id']==member['participant'] and r['task_id']==t['id']]
                best=max((r['total'] or 0 for r in rs),default=0)
                item[f"Lab {t['id']}"]=f'{best:g}/100' if any(r['total'] is not None for r in rs) else (rs[0]['status'] if rs else '—')
            table.append(item)
        st.dataframe(table,hide_index=True,use_container_width=True)
    with history:
        st.download_button('Download all submissions and scores (CSV)',storage.export_csv(token),'workshop_results.csv','text/csv')
        if rows:
            def format_attempt(aid):
                r = next(row for row in rows if row['id'] == aid)
                return f"{r['user_id']} — Lab {r['task_id']} — Score: {r['total']} ({r['status']})"
            selected=st.selectbox('Inspect an attempt', [r['id'] for r in rows], format_func=format_attempt)
            row=next(r for r in rows if r['id']==selected)
            st.code(row['prompt'],language=None)
            c1, c2, _ = st.columns([1, 1, 4])
            if c1.button('Force Pass', key=f"pass_{row['id']}"):
                storage.override_attempt_status(token, row['id'], 'passed')
                st.rerun()
            if c2.button('Force Retry', key=f"retry_{row['id']}"):
                storage.override_attempt_status(token, row['id'], 'revise')
                st.rerun()
            st.json(json.loads(row['automatic']))
        if rows:st.dataframe([{k:r[k] for k in ['id','user_id','task_id','status','auto_score','total','created']} for r in rows],hide_index=True)
else:
    passed={r['task_id'] for r in rows if r['status']=='passed'}
    st.title(f"{user['id']} · Your workspace")
    st.progress(len(passed)/8,text=f'{len(passed)} of 8 labs passed')
    if len(passed)==8:st.success('Workshop complete! Save your prompt journal and apply one technique to your work this week.')
    available=[t['id'] for t in TASKS if set(range(1,t['id'])).issubset(passed)]
    with st.sidebar:
        for t in TASKS:st.write(('✓' if t['id'] in passed else '○' if t['id'] in available else '🔒')+f" {t['id']}. {t['title']}")
    task_id=st.selectbox('Choose an unlocked lab',available,index=len(available)-1,format_func=lambda n:f"Lab {n}: {TASKS[n-1]['title']}")
    task=TASKS[task_id-1]
    st.subheader(task['title'])
    if not task.get('hide_concept'):st.write(task['concept'])
    st.info(task['ai_brief'])
    if 'ai_brief_fa' in task:
        html_fa = f"""<div dir="rtl" style="text-align: right; direction: rtl; padding: 1em; border-radius: 0.5em; background-color: rgba(43, 153, 56, 0.15); border: 1px solid rgba(43, 153, 56, 0.3); margin-bottom: 1rem;">
        <strong>🇮🇷 ترجمه سناریو:</strong><br><br>{task['ai_brief_fa']}
        </div>"""
        st.markdown(html_fa, unsafe_allow_html=True)
    draft=storage.get_draft(token,task_id)
    with st.form(f'lab_{task_id}'):
        prompt=st.text_area('Your prompt',value=draft.get('prompt',''),height=280,max_chars=20000,help='Submit instructions for the model, not the final answer. For example: Write an empathetic support reply under 100 words using the following facts…')
        quiz=st.radio(task['quiz'],range(3),format_func=lambda n:task['options'][n],index=None,key=f'quiz_{task_id}')
        a,b=st.columns(2);save=a.form_submit_button('Save draft');send=b.form_submit_button('Submit for evaluation',type='primary')
    if save or send:
        try:
            storage.save_draft(token,task_id,prompt,'','')
            if send and quiz is None:
                st.error('Answer the concept question before submitting.')
            elif send:
                with st.spinner('Evaluating your prompt…'):
                    storage.submit_prompt(token,task_id,prompt,quiz)
                st.rerun()
            else:st.success('Draft saved.')
        except (ValueError,PermissionError) as e:st.error(str(e))
    st.subheader('Feedback and attempt history')
    if st.button('Refresh feedback'):st.rerun()
    own=[r for r in rows if r['task_id']==task_id]
    if not own:st.write('No submissions for this lab yet.')
    for row in own:
        with st.expander(f"Attempt #{row['id']} · {row['status']} · "+(f"{row['total']:g}/100" if row['total'] is not None else f"{row['auto_score']:g}/40 automatic points"),expanded=row==own[0]):
            result=json.loads(row['automatic'])
            if result.get('mode')=='ai_prompt_v1':
                st.caption(f"Evaluator: {result['model']} · rubric ai_prompt_v1")
                st.write(result['summary'])
                if 'quiz' in result:
                    concept=result['quiz']
                    st.write('Concept question: '+concept['question'])
                    st.write('Your answer: '+concept['selected_text'])
                    if concept['correct']:st.success('Concept check: correct.')
                    else:st.warning('Concept check: incorrect. Review the lesson and choose again.')
                for criterion in result['criteria']:
                    st.markdown(f"**{criterion['score']}/{criterion.get('maximum',25)} · {criterion['criterion']}**")
                    st.write(criterion['feedback']);st.caption('Evidence: '+criterion['evidence'])
                for key,label in [('strengths','Strengths'),('issues','Issues'),('improvements','Suggested improvements')]:
                    st.markdown('**'+label+'**')
                    for item in result[key]:st.write('• '+item)
                if row['status']=='passed':st.success('Passed. The next lab is unlocked.')
                else:st.warning('Not passed. You need a prompt score of at least 70 and a correct concept answer. Review the feedback and retry.')
                with st.expander('Submitted prompt'):st.code(row['prompt'],language=None)
            else:
                st.caption('Historical submission · previous manual scoring policy')
                for check in result['checks']:
                    st.write(f"{check['label']}: {check['points']:g}/{check['maximum']:g} · {check['feedback']}")
                if row['feedback']:st.write(row['feedback'])
    journal=json.dumps([{k:r[k] for k in ['task_id','prompt','status','total','feedback','automatic']} for r in rows],indent=2,ensure_ascii=False)
    st.download_button('Download my prompt journal',journal,f"{user['id']}_journal.json",'application/json')
