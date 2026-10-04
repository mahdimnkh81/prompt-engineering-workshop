# 🧪 Prompt Engineering Workshop & Interactive Lab

An interactive, multi-user web application built with **Streamlit** to teach advanced Prompt Engineering. Unlike traditional slide-based courses, this platform provides a hands-on lab where participants write prompts and receive **real-time, automated grading and feedback** from an AI evaluator (Claude / AvalAI) based on strict task-specific rubrics.

## ✨ Features

- **Interactive Labs:** 7 structured exercises covering foundational to advanced techniques (Role Prompting, Few-shot Examples, Chain-of-Thought, XML Structuring, Prompt Chaining, etc.).
- **Live AI Evaluator:** Submissions are automatically graded by an LLM against a hidden rubric. Participants receive detailed feedback (Strengths, Issues, Suggested Improvements) and a score out of 100.
- **Instructor Dashboard:** A dedicated real-time dashboard for instructors to monitor class progress, review attempts, and access the master answer key.
- **Concurrent & Refresh-Safe:** Supports 20+ simultaneous participants. Utilizes SQLite in WAL mode for safe concurrent writes and URL-based session tokens so participants don't lose access upon browser refresh.
- **Bilingual Support:** Workshop briefs and scenarios are provided in both English and Persian.

## 🛠️ Tech Stack

- **Frontend & Backend:** [Streamlit](https://streamlit.io/) (Python)
- **Database:** SQLite3 (with WAL mode for concurrency)
- **AI Integration:** Anthropic API / AvalAI API
- **Testing:** Pytest

## 🚀 Installation & Setup

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/prompt-engineering-workshop.git
cd prompt-engineering-workshop
```

**2. Create and activate a virtual environment:**
```bash
# On Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# On Windows
python -m venv .venv
.venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Configure API Keys:**
The app uses an LLM to evaluate participant prompts. You need to provide an API key for Anthropic or AvalAI. You can set this as an environment variable or create a `.streamlit/secrets.toml` file:

```toml
# .streamlit/secrets.toml
ANTHROPIC_API_KEY = "your-api-key-here"
# OR
AVALAI_API_KEY = "your-avalai-api-key"
```

## 🗄️ Database Initialization

Before running the app for the first time, initialize the SQLite database and generate participant credentials:

```bash
python storage.py
```
*Note: This will generate 20 participant accounts and 1 instructor account. The credentials will be saved locally in `data/credentials.csv`.*

If you want to use custom usernames and passwords, you can modify or run the `import_custom_users.py` script.

## 🏃‍♂️ Running the Application

To start the Streamlit server:

```bash
streamlit run app.py
```

For production deployment (e.g., on a Linux VPS), it is recommended to run the app in the background and force the light theme:

```bash
# Enforce light theme for all users
echo -e "[theme]\nbase=\"light\"" > .streamlit/config.toml

# Run in background
nohup python3 -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > server.log 2>&1 &
```

## 📚 Curriculum Overview

1. **Set the scene:** Defining Role, Audience, Tone, and Format.
2. **Few-shot examples:** Handling edge cases (e.g., PII & Content Moderation).
3. **Chain-of-thought (CoT):** Forcing step-by-step reasoning for debugging logs.
4. **Structured Output:** Using XML tags and JSON skeletons to format complex extraction.
5. **Constraints:** Iterative refinement and negative constraints.
6. **Simulating conversation:** Interview-style prompts for system architecture.
7. **Roles, chaining, and self-evaluation:** Multi-turn prompt chains forcing the AI to critique its own drafts.

## 🔒 Security & Privacy
- **No plaintext passwords:** All passwords are mathematically hashed with random salts using `hashlib.scrypt` before being stored in SQLite.
- **Session isolation:** Participants can only access their own workspace and drafts.

## 📄 License
This project is licensed under the MIT License.
