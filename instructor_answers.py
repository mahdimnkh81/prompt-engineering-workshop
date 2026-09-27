"""Instructor reference answers; never included in participant UI or judge requests."""
from reference_answers import ANSWERS, RATIONALES, EXPECTED

def get_answer(token, task_id):
    import storage
    from curriculum import TASKS
    if storage.identity(token)['role'] != 'instructor':
        raise PermissionError('Instructor access required.')
    if type(task_id) is not int or task_id not in range(1,9):
        raise ValueError('Unknown task.')
    task=TASKS[task_id-1]
    return dict(prompt=ANSWERS[task_id-1],rationale=RATIONALES[task_id-1],expected=EXPECTED[task_id-1],question=task['quiz'],answer=task['options'][task['answer']],answer_number=task['answer']+1)
