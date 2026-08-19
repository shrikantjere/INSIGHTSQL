import re

FORBIDDEN = [r"\bDROP\b", r"\bDELETE\b", r"\bUPDATE\b", r"\bINSERT\b", r"\bALTER\b", r"\bTRUNCATE\b", r";", r"\bATTACH\b", r"\bDETACH\b"]


def is_safe_sql(sql: str) -> bool:
    if not sql or not isinstance(sql, str):
        return False
    s = sql.strip()
    # Only single statement allowed
    if s.count(";") > 0:
        return False
    # Must start with SELECT (allow leading parentheses and whitespace)
    if not re.match(r"^\s*(SELECT)\b", s, re.IGNORECASE):
        return False
    # Forbid dangerous keywords
    for pat in FORBIDDEN:
        if re.search(pat, s, re.IGNORECASE):
            return False
    return True


if __name__ == "__main__":
    tests = [
        "SELECT * FROM employees",
        "DROP TABLE employees",
        "SELECT * FROM employees; DELETE FROM employees",
        "  SELECT name FROM employees WHERE salary > 100000",
    ]
    for t in tests:
        print(t, is_safe_sql(t))
