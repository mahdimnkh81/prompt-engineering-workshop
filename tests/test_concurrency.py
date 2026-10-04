"""Concurrency and refresh-resilience checks for a live 20-participant workshop."""
import csv
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pytest
import storage
from curriculum import TASKS
from reference_answers import ANSWERS


@pytest.fixture
def accounts(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, 'DB', tmp_path / 'workshop.sqlite3')
    assert storage.initialize()
    return list(csv.DictReader((tmp_path / 'credentials.csv').open()))


def test_twenty_participants_submit_simultaneously(accounts, monkeypatch):
    """20 users log in, save drafts, and submit at the same moment with a slow grader.

    Odd-numbered participants get a passing score, even-numbered a failing one, so any
    mix-up between users (wrong prompt, wrong score, wrong owner) is detected.
    """
    from test_ai import result

    def slow_grader(task, prompt):
        time.sleep(0.5)  # simulate a network call while other users keep writing
        number = int(prompt.split('#')[1].split()[0])
        return result(20 if number % 2 else 5)

    monkeypatch.setattr('ai_evaluation.grade_prompt', slow_grader)
    participants = [r for r in accounts if r['username'].startswith('participant')]
    assert len(participants) == 20
    barrier = threading.Barrier(len(participants))

    def workshop_session(record):
        number = int(record['username'][-2:])
        token = storage.login(record['username'], record['password'])
        assert token
        prompt = f"Participant #{number} unique prompt. " + ANSWERS[0]
        for i in range(5):  # repeated draft saves, like users typing and saving
            storage.save_draft(token, 1, prompt + f' v{i}', '', '')
        barrier.wait()  # everyone clicks Submit at the same moment
        storage.submit_prompt(token, 1, prompt, TASKS[0]['answer'])
        return record['username'], token, prompt, number

    with ThreadPoolExecutor(max_workers=len(participants)) as pool:
        outcomes = list(pool.map(workshop_session, participants))

    for username, token, prompt, number in outcomes:
        own = storage.attempts(token)
        assert len(own) == 1, f'{username} should have exactly one attempt'
        attempt = own[0]
        assert attempt['user_id'] == username
        assert attempt['prompt'] == prompt
        assert attempt['status'] == ('passed' if number % 2 else 'revise')
        assert storage.get_draft(token, 1)['prompt'] == prompt
        assert storage.identity(token)['id'] == username  # still signed in

    instructor = next(r for r in accounts if r['username'] == 'instructor')
    admin = storage.login(instructor['username'], instructor['password'])
    assert len(storage.attempts(admin)) == 20
    assert sum(r['passed'] for r in storage.roster(admin)) == 10


def test_refresh_keeps_participant_signed_in(accounts):
    from streamlit.testing.v1 import AppTest
    record = next(r for r in accounts if r['username'] == 'participant01')
    token = storage.login(record['username'], record['password'])

    # A browser refresh starts a brand-new Streamlit session with only the URL.
    app = AppTest.from_file(str(storage.ROOT / 'app.py'))
    app.query_params['s'] = token
    app.run()
    assert not app.exception
    assert app.session_state['token'] == token
    assert len(app.text_area) == 1  # workspace visible, not the login form
    assert any(f'of {len(TASKS)} labs passed' in (p.proto.text or '') for p in app.get('progress'))

    # Tampered or expired tokens fall back to the login page.
    bad = AppTest.from_file(str(storage.ROOT / 'app.py'))
    bad.query_params['s'] = 'not-a-real-token'
    bad.run()
    assert not bad.exception
    assert 'token' not in bad.session_state
    assert len(bad.text_input) == 2

    # After sign-out the old URL no longer works.
    storage.logout(token)
    stale = AppTest.from_file(str(storage.ROOT / 'app.py'))
    stale.query_params['s'] = token
    stale.run()
    assert 'token' not in stale.session_state
