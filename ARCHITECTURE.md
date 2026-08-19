# Architecture Overview

Components:
- Streamlit frontend (`app.py`)
- OpenAI model for NL→SQL (`prompt_templates.SQL_SYSTEM_PROMPT`)
- SQLite database (`employee_management.db`)
- Validation layer (`sql_validator.py`)

Data flow:
1. User types question in UI.
2. App sends question + schema prompt to OpenAI.
3. OpenAI returns SQL.
4. App validates SQL and executes it on SQLite.
5. Results displayed to user with SQL visible.

Security:
- Only allow SELECT statements; block dangerous keywords and multiple statements.
