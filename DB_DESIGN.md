# Database Design

ER Diagram (text):

employees(employee_id) --(department_id)--> departments(department_id)
employees(employee_id) --(employee_id)--> employee_projects(employee_id) --(project_id)--> projects(project_id)

Tables:
- departments(department_id INTEGER PK, department_name TEXT)
- employees(employee_id INTEGER PK, name TEXT, department_id INTEGER FK, city TEXT, salary REAL, joined_date TEXT)
- projects(project_id INTEGER PK, project_name TEXT, budget REAL)
- employee_projects(employee_id INTEGER FK, project_id INTEGER FK)

Sample data: included in `create_db.py` — 5 departments, 20 employees, 10 projects.
