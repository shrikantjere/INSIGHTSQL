from sql_validator import is_safe_sql


def test_valid_select():
    assert is_safe_sql("SELECT * FROM employees")
    assert is_safe_sql("  SELECT name FROM employees WHERE salary > 100000")


def test_reject_dangerous():
    assert not is_safe_sql("DROP TABLE employees")
    assert not is_safe_sql("SELECT * FROM employees; DELETE FROM employees")
    assert not is_safe_sql("INSERT INTO employees VALUES (1)")
