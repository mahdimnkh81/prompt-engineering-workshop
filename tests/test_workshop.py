import csv
import json
import pytest
import storage
from curriculum import AGENDA, TASKS
from reference_answers import ANSWERS

PROMPT=ANSWERS[0]

@pytest.fixture
def accounts(tmp_path,monkeypatch):
    monkeypatch.setattr(storage,'DB',tmp_path/'workshop.sqlite3')
    assert storage.initialize()
    records=list(csv.DictReader((tmp_path/'credentials.csv').open()))
    tokens={r['username']:storage.login(r['username'],r['password']) for r in records}
    return records,tokens

def test_schedule():assert sum(x[1] for x in AGENDA)==180

def test_auth_and_isolation(accounts,monkeypatch):
    from test_ai import result
    monkeypatch.setattr('ai_evaluation.grade_prompt',lambda *args:result(20))
    records,tokens=accounts
    assert len(records)==21
    assert storage.login('participant01','incorrect') is None
    assert storage.login('nonexistent','incorrect') is None
    p=tokens['participant01'];q=tokens['participant02']
    storage.submit_prompt(p,1,PROMPT,0)
    assert len(storage.attempts(p))==1
    assert storage.attempts(q)==[]
    with pytest.raises(PermissionError):storage.export_csv(p)
    with pytest.raises(PermissionError):storage.roster(p)
    storage.logout(p)
    with pytest.raises(PermissionError):storage.attempts(p)

def test_drafts_persist_and_init_preserves(accounts):
    _,t=accounts;p=t['participant01']
    storage.save_draft(p,1,PROMPT,'','')
    assert not storage.initialize()
    assert storage.get_draft(p,1)['prompt']==PROMPT
    assert storage.get_draft(t['participant02'],1)=={}
    assert len(storage.roster(t['instructor']))==20

def test_all_labs_complete(accounts,monkeypatch):
    from test_ai import result
    monkeypatch.setattr('ai_evaluation.grade_prompt',lambda *args:result(20))
    _,t=accounts;p=t['participant01'];admin=t['instructor']
    for task,prompt in zip(TASKS,ANSWERS):
        storage.submit_prompt(p,task['id'],prompt,task['answer'])
    assert storage.roster(admin)[0]['passed']==len(TASKS)
    assert len(storage.attempts(p))==len(TASKS)

def test_streamlit_login_and_dashboard(accounts,monkeypatch):
    from streamlit.testing.v1 import AppTest
    from test_ai import result
    monkeypatch.setattr('ai_evaluation.grade_prompt',lambda task,prompt:result(20))
    records,tokens=accounts
    app=AppTest.from_file(str(storage.ROOT/'app.py')).run()
    assert not app.exception
    record=next(r for r in records if r['username']=='participant01')
    app.text_input[0].set_value(record['username']);app.text_input[1].set_value(record['password'])
    app.button[0].click().run()
    assert not app.exception
    assert not any(t.label=='Instructor answer key' for t in app.tabs)
    assert len(app.text_area)==1
    assert len(app.radio)==1
    assert len(app.radio[0].options)==3
    app.radio[0].set_value(0)
    app.text_area[0].set_value(PROMPT)
    next(b for b in app.button if b.label=='Submit for evaluation').click().run()
    assert not app.exception
    assert storage.attempts(app.session_state['token'])[0]['status']=='passed'
    assert len(app.selectbox[0].options)==2
    instructor=AppTest.from_file(str(storage.ROOT/'app.py'))
    instructor.session_state['token']=tokens['instructor'];instructor.run()
    assert not instructor.exception
    assert instructor.metric[1].value=='0'
    assert any(t.label=='Instructor answer key' for t in instructor.tabs)
    assert any('Option 1:' in item.value for item in instructor.success)
