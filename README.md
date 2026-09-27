# Prompt Engineering Workshop — AI evaluation

A three-hour workshop based on the supplied PDF: 41 PowerPoint slides, eight labs, and 20 authenticated participant workspaces.

## New submission flow

Participants submit **their prompt and a three-option concept answer**. The server asks `gpt-6-astra` through AvalAI to evaluate it against four task-specific weighted criteria totaling 100 points. It returns English feedback, quoted evidence, strengths, problems, and actionable improvements. The evaluator assesses the prompt rather than executing it or generating the assignment answer. No external chat tool, pasted output, reflection, or manual instructor approval is required. Each lab includes its original three-option concept question.

The server validates the returned structure and computes the total itself. **A prompt score of at least 70/100 AND a correct concept answer unlock the next lab automatically**. Lower scores remain locked; participants revise and retry. A failed API call never creates a zero grade or unlocks a task; the draft remains saved. Earlier attempts and earned passes are preserved, including historical manual assessments.

## Configure AvalAI

From `/mnt/data/WorkShop`, copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and replace the placeholder locally:

```toml
AVALAI_API_KEY = "your-real-key"
AVALAI_BASE_URL = "https://api.avalai.ir/v1"
AVALAI_MODEL = "gpt-6-astra"
```

Alternatively set the same environment variables on the server. Environment variables take precedence. `avalai_api_key` is also accepted as the secrets-file key name. The key stays on the server and is not included in browser forms, stored assessments, or exports. The secrets file is excluded from Git. Do not paste your key into chat.

The integration uses an HTTP POST to `/chat/completions`, equivalent to the supplied ChatOpenAI configuration, without a LangChain dependency. It sends `model` and `messages`; temperature is omitted as requested. Provider model availability and account credit must be confirmed with a real key. Each submission makes one API call, with no automatic paid retries.

```bash
cd /mnt/data/WorkShop
source .venv/bin/activate
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Open `http://localhost:8501`; participants use `http://HOST_IP:8501/?participant=participant01`, etc. Credentials for 20 participants and the instructor are in private `data/credentials.csv`. Distribute each participant's own row only. For a fresh install, create a venv, install requirements, and run `python storage.py --base-url http://HOST_IP:8501`. Existing accounts are preserved. `WORKSHOP_DB` selects another cohort database; use a separate directory for each cohort.

The instructor dashboard shows class progress, all attempts, prompts, full model feedback, and CSV export. Historical attempts remain visible in the export and attempt history. Participants see only their own drafts, scores, feedback, and downloadable journals.

## Files

- `ai_evaluation.py`: provider configuration, evaluator instructions, API client, response validation.
- `curriculum.py`: current tasks, concept answers, prompt briefs, weights, and AI rubrics.
- `storage.py`: authentication, persistence, automatic progression.
- `materials/prompt_engineering_3_hour_workshop.pptx`: regenerated slides with speaker notes.
- `materials/facilitator_guide.md`, `participant_lab_book.md`, `speaker_notes.md`: updated teaching materials.

## Evaluation limitations and operations

AI grading can vary and is not a guarantee that a prompt will produce correct answers. Calibrate on strong, weak, and manipulative submissions before class. Participant prompts are sent to AvalAI; usernames, passwords, and other participants' submissions are not sent. Attempts to manipulate grading are explicitly treated as untrusted data, but prompt-injection resistance cannot be guaranteed.

This setup is intended for a trusted workshop network. Public hosting requires HTTPS and deployment-level rate/access controls. SQLite uses WAL and transactional writes; network evaluation does not hold a database write lock. Sessions last 12 hours. Stop the app before copying the entire private data directory for backup.

## Test and regenerate

```bash
python -m pytest -q
python build_materials.py
```

Tests mock the provider to verify request formatting, score validation, failure handling, access isolation, progression, and Streamlit flow without API costs. Real provider connectivity must also be tested after configuring the key.

## Instructor answer key

Sign in as instructor and open **Instructor answer key**. Each of the eight labs includes a reference prompt, rationale, rubric, expected behavior/example output, and the correct concept-question option. References are not unique correct prompts or guaranteed model scores. The answer-key accessor enforces instructor authorization; the participant interface and evaluator requests do not include these references.

## Lab 1: scene-setting for hiring

Participants write a LinkedIn Python recruiting prompt. Weights are role 20, audience 20, tone 20, format 40. Format allocates 20 to structure and 20 to an explicit example/analogy instruction; omitting that instruction caps format at 20 but does not automatically fail a prompt. The threshold remains 70 plus the correct concept answer. The presentation demonstrates the technique with an API explanation for a nontechnical client, separate from the participant hiring exercise. Old curriculum rubric fields have been removed; old manual assessments remain archived but the manual grading form is retired.
