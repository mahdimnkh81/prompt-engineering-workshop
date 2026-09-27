# Facilitator guide — AI prompt assessment

20 participants · 180 minutes · source: original nine-page PDF.

| Time | Minutes | Activity |
|---|---:|---|
| 00:00–00:10 | 10 | Welcome, baseline, login |
| 00:10–00:30 | 20 | 1 · Context and specificity |
| 00:30–00:50 | 20 | 2 · Few-shot examples |
| 00:50–01:10 | 20 | 3 · Decomposition and verification |
| 01:10–01:30 | 20 | 4 · Structured outputs |
| 01:30–01:40 | 10 | Break |
| 01:40–01:55 | 15 | 5 · Constraints and iteration |
| 01:55–02:10 | 15 | 6 · Interview-style prompting |
| 02:10–02:30 | 20 | 7 · Roles, chaining, and critique |
| 02:30–02:50 | 20 | 8 · Capstone and evaluation |
| 02:50–03:00 | 10 | Share results and prompt journal |

## Before class

Configure AVALAI_API_KEY in the server environment or .streamlit/secrets.toml; see README.md. The configured provider is AvalAI, model gpt-6-astra, endpoint https://api.avalai.ir/v1. Test a real submission before class and confirm model access and sufficient provider credit. Give each participant only their individual credential row. Open the PowerPoint in presenter mode.

## Participant flow

Participants write a prompt and answer the original three-option concept question. They do not use an external chat model, paste a generated answer, or provide a reflection. The server sends their prompt as untrusted data to a separate evaluator instruction containing the task-specific rubric. The evaluator assesses the prompt without executing it and provides English feedback, evidence, issues, and improvements.

## Scoring

Lab 1: role 20, audience 20, tone 20, format 40 (structure 20 + explicit example/analogy 20). Missing the example/analogy request caps format at 20/40, not automatic failure. Other labs: four criteria × 25 = 100. Anchors: 0 absent/contradictory, 5 severe gaps, 10 partial, 15 mostly specified with important gaps, 20 clear with minor gaps, 25 complete. The server validates the response and sums the criterion scores itself. At least 70 plus a correct concept answer unlocks the next task immediately; otherwise participants must retry. The concept question is checked by the server and adds no points to the prompt score. API failures assign no score and preserve the draft. Existing earned passes and historical manual attempts remain available.

Model grading is an assessment aid, not proof of real output reliability. It can vary or misjudge a prompt. Review a sample of scores before class, discuss disputed feedback, and help participants revise. New submissions no longer require instructor approval. Historical attempts remain available in the dashboard history.

## Timing and facilitation

Use each lab's teaching, practice, and retry allocations in the slide notes. During practice, watch class progress and help participants who remain blocked. Strict mastery gates may mean some need follow-up after the three-hour session. Keep the scheduled break.

## Source mapping

Labs 1–8 map to PDF pages 1–3, 3, 3–4, 4, 5, 5–6, 6–7, and 7–9. The source's unsupported 80% claim is omitted. Verification is taught through concise checkable calculations. Participant code is never executed by the server.
