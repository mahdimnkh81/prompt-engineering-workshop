import ai_evaluation as ai
from curriculum import TASKS

prompt = """
Extract users and tasks from meeting transcripts. The output must be exactly a JSON object containing a "users" array and a "tasks" array. Link them using a numeric userId.

"users": [
  { "userId": 1, "name": "..." }
],
"tasks": [
  {
    "taskDescription": "...",
    "deadline": "... or null",
    "assignedTo": 1
  }
]
Meeting transcript: [transcript]
"""

try:
    result = ai.grade_prompt(TASKS[3], prompt)
    print("Success:", result)
except Exception as e:
    import traceback
    print("Failed!")
    traceback.print_exc()
