import sqlite3
import types
import os
import pandas as pd
import pytest

import app
from sql_validator import is_safe_sql


class FakeChoice:
    def __init__(self, content: str):
        self.message = types.SimpleNamespace(content=content)


class FakeResponse:
    def __init__(self, content: str):
        self.choices = [FakeChoice(content)]


class FakeOpenAIClient:
    def __init__(self, content: str = None, raise_exc: Exception = None):
        self._content = content
        self._raise = raise_exc

    class Chat:
        def __init__(self, parent):
            self.parent = parent

        class Completions:
            def __init__(self, parent):
                self.parent = parent

            def create(self, **kwargs):
                if self.parent._raise:
                    raise self.parent._raise
                return FakeResponse(self.parent._content)

        @property
        def completions(self):
            return FakeOpenAIClient.Chat.Completions(self.parent)

    @property
    def chat(self):
        return FakeOpenAIClient.Chat(self)


def test_generate_sql_with_fake_client(monkeypatch):
    fake = FakeOpenAIClient(content="SELECT name FROM employees WHERE city='Bangalore'")
    monkeypatch.setattr(app, "OPENAI_CLIENT", fake)
    sql = app.generate_sql("Show employees in Bangalore", app.SQL_SYSTEM_PROMPT)
    assert "SELECT" in sql.upper()
    assert "employees" in sql


def test_generate_sql_openai_failure(monkeypatch):
    fake = FakeOpenAIClient(raise_exc=RuntimeError("API down"))
    monkeypatch.setattr(app, "OPENAI_CLIENT", fake)
    with pytest.raises(Exception):
        app.generate_sql("Any question", app.SQL_SYSTEM_PROMPT)


def test_sql_validation_positive_and_negative():
    assert is_safe_sql("SELECT name FROM employees")
    assert not is_safe_sql("DROP TABLE employees")
    # Obfuscated attempt
    assert not is_safe_sql("SELECT name FROM employees; DROP TABLE departments")
    # Comment injection should be rejected due to semicolon or forbidden keywords
    assert not is_safe_sql("SELECT name FROM employees -- ; DROP TABLE employees")


def test_execute_sql_success(tmp_path):
    db_file = tmp_path / "test.db"
    conn = sqlite3.connect(str(db_file))
    cur = conn.cursor()
    cur.execute("CREATE TABLE employees(employee_id INTEGER PRIMARY KEY, name TEXT, city TEXT, salary REAL)")
    cur.executemany("INSERT INTO employees(name, city, salary) VALUES (?,?,?)",
                    [("Alice", "Bangalore", 100000), ("Bob", "Delhi", 90000)])
    conn.commit()
    conn.close()

    df = app.execute_sql(str(db_file), "SELECT name, city FROM employees ORDER BY name")
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2


def test_execute_sql_schema_error(tmp_path):
    db_file = tmp_path / "test2.db"
    conn = sqlite3.connect(str(db_file))
    conn.close()
    with pytest.raises(Exception):
        # table does not exist
        app.execute_sql(str(db_file), "SELECT * FROM non_existing_table")


def test_empty_and_invalid_question_flow(monkeypatch):
    # OpenAI returns empty result
    fake_empty = FakeOpenAIClient(content="")
    monkeypatch.setattr(app, "OPENAI_CLIENT", fake_empty)
    sql = app.generate_sql("", app.SQL_SYSTEM_PROMPT)
    assert sql == ""
    assert not is_safe_sql(sql)

    # OpenAI returns a dangerous SQL
    fake_bad = FakeOpenAIClient(content="DELETE FROM employees")
    monkeypatch.setattr(app, "OPENAI_CLIENT", fake_bad)
    sql2 = app.generate_sql("Remove employees", app.SQL_SYSTEM_PROMPT)
    assert "DELETE" in sql2.upper()
    assert not is_safe_sql(sql2)
