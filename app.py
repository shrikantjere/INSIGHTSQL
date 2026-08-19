import os
import sqlite3
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from sql_validator import is_safe_sql
from prompt_templates import SQL_SYSTEM_PROMPT

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
DB_PATH = os.getenv("DB_PATH", "employee_management.db")

try:
    from openai import OpenAI
    OPENAI_CLIENT = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else OpenAI()
except Exception:
    import openai
    OPENAI_CLIENT = None
    openai.api_key = OPENAI_API_KEY


def generate_sql(question: str, schema_prompt: str) -> str:
    messages = [
        {"role": "system", "content": schema_prompt},
        {"role": "user", "content": question},
    ]

    if OPENAI_CLIENT is not None:
        resp = OPENAI_CLIENT.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=512,
            temperature=0,
        )
        try:
            sql = resp.choices[0].message.content.strip()
        except Exception:
            sql = resp.choices[0]["message"]["content"].strip()
    else:
        resp = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=512,
            temperature=0,
        )
        sql = resp.choices[0].message.content.strip()

    return sql


def execute_sql(db_path: str, sql: str):
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(sql, conn)
    finally:
        conn.close()
    return df


def main():
    st.set_page_config(page_title="InsightSQL - Workforce Analytics", layout="wide")
    st.title("InsightSQL — AI Powered Workforce Analytics")

    st.sidebar.header("Settings")
    if not OPENAI_API_KEY:
        st.sidebar.error("Set OPENAI_API_KEY in environment to enable SQL generation.")
    st.sidebar.write(f"DB: {DB_PATH}")

    st.markdown("Ask natural language questions about the company HR data. Only SELECT statements are allowed.")

    question = st.text_input("Ask a question:")
    col1, col2 = st.columns([2, 1])

    with col1:
        if st.button("Generate & Run") and question:
            with st.spinner("Generating SQL..."):
                try:
                    sql = generate_sql(question, SQL_SYSTEM_PROMPT)
                except Exception as e:
                    st.error(f"SQL generation failed: {e}")
                    return

            st.subheader("Generated SQL")
            st.code(sql, language="sql")

            if not is_safe_sql(sql):
                st.error("Generated SQL is not allowed. Only single SELECT queries are permitted.")
                return

            try:
                df = execute_sql(DB_PATH, sql)
            except Exception as e:
                st.error(f"SQL execution error: {e}")
                return

            st.subheader("Results")
            st.dataframe(df)

            st.subheader("Insights")
            st.write(f"Rows returned: {len(df)}")
            if not df.empty:
                numeric = df.select_dtypes(include=["number"]).columns.tolist()
                if numeric:
                    st.write(df[numeric].describe())

            history = st.session_state.get("history", [])
            history.insert(0, {"question": question, "sql": sql, "rows": len(df)})
            st.session_state["history"] = history[:50]

    with col2:
        st.subheader("Query History")
        for item in st.session_state.get("history", []):
            with st.expander(item["question"][:80]):
                st.write(item)


if __name__ == "__main__":
    main()
