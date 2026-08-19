# InsightSQL - Product Requirements Document

Executive Summary
-----------------
InsightSQL enables non-technical business users to query HR data using natural language. The assistant converts questions to SQL, executes them against a SQLite database, and returns results and business-friendly insights.

Business Objectives
-------------------
- Reduce time-to-insight for HR stakeholders.
- Minimize dependency on engineering for routine reports.
- Ensure safe execution by preventing destructive SQL.

Stakeholders
------------
- HR Managers, Department Heads, Placement Officers, Administrators, Business Analysts
- Engineering (maintain app)
- Product Manager

Functional Requirements
-----------------------
1. Accept natural language questions.
2. Generate SQL (SELECT only) from questions.
3. Validate generated SQL for safety.
4. Execute against SQLite and return results.
5. Display generated SQL and maintain history.
6. Explain results in business terms.

Non Functional Requirements
---------------------------
- Response latency under 3 seconds (for simple queries).
- Secure: no destructive SQL allowed.
- Audit logs for queries.

User Stories
------------
- As an HR manager, I can ask "How many employees work in Bangalore?" and get an immediate answer.

Acceptance Criteria
-------------------
- Natural language input returns a valid SQL and results.
- Any non-SELECT or multi-statement SQL is rejected.

Project Risks
-------------
- Incorrect SQL generation (hallucinations).
- OpenAI API availability and cost.

Future Enhancements
-------------------
- Role-based access control, multi-database support, caching, analytics dashboards.
