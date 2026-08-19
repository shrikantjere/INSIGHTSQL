# InsightSQL

AI-powered Workforce Analytics Assistant. Ask questions in English and get answers from a SQLite HR database.

Quickstart
----------
1. Create virtual env and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create the database (will create `employee_management.db`):

```bash
python create_db.py
```

3. Set your OpenAI API key in env:

```bash
export OPENAI_API_KEY="sk-..."
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

Notes
-----
- The app enforces a strict validation: only single SELECT statements are allowed.
- The SQL generation system prompt lives in `prompt_templates.py` and follows the Module 5 requirements.
# INSIGHTSQL