import sqlite3
import os
from datetime import date

DB_PATH = os.getenv("DB_PATH", "employee_management.db")


def create_tables(conn):
    cur = conn.cursor()
    cur.executescript(
        '''
        CREATE TABLE IF NOT EXISTS departments(
            department_id INTEGER PRIMARY KEY,
            department_name TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS employees(
            employee_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            department_id INTEGER,
            city TEXT,
            salary REAL,
            joined_date TEXT,
            FOREIGN KEY(department_id) REFERENCES departments(department_id)
        );

        CREATE TABLE IF NOT EXISTS projects(
            project_id INTEGER PRIMARY KEY,
            project_name TEXT NOT NULL,
            budget REAL
        );

        CREATE TABLE IF NOT EXISTS employee_projects(
            employee_id INTEGER,
            project_id INTEGER,
            PRIMARY KEY(employee_id, project_id),
            FOREIGN KEY(employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY(project_id) REFERENCES projects(project_id)
        );
        '''
    )
    conn.commit()


def seed_sample_data(conn):
    cur = conn.cursor()
    departments = [
        (1, 'Engineering'),
        (2, 'Human Resources'),
        (3, 'Sales'),
        (4, 'Marketing'),
        (5, 'Finance'),
    ]
    cur.executemany('INSERT OR IGNORE INTO departments VALUES (?,?)', departments)

    employees = [
        (1, 'Alice Johnson', 1, 'Bangalore', 120000, '2021-06-15'),
        (2, 'Bob Smith', 1, 'Hyderabad', 110000, '2020-03-22'),
        (3, 'Carol Lee', 2, 'Bangalore', 90000, '2019-11-05'),
        (4, 'David Kim', 3, 'Chennai', 95000, '2022-01-10'),
        (5, 'Eve Torres', 4, 'Bangalore', 105000, '2023-02-14'),
        (6, 'Frank Wright', 5, 'Mumbai', 98000, '2018-09-04'),
        (7, 'Grace Park', 1, 'Bangalore', 125000, '2022-07-25'),
        (8, 'Hank Aaron', 3, 'Pune', 88000, '2020-12-01'),
        (9, 'Ivy Chen', 4, 'Bangalore', 102000, '2021-08-19'),
        (10, 'Jack Black', 2, 'Delhi', 85000, '2017-04-30'),
        (11, 'Karen Miller', 1, 'Bangalore', 115000, '2019-01-20'),
        (12, 'Leo Wilson', 5, 'Chennai', 94000, '2023-05-11'),
        (13, 'Mona Patel', 3, 'Bangalore', 93000, '2022-10-02'),
        (14, 'Ned Stark', 4, 'Hyderabad', 99000, '2021-03-03'),
        (15, 'Olivia Brown', 2, 'Mumbai', 87000, '2020-06-06'),
        (16, 'Paul Adams', 1, 'Bangalore', 130000, '2016-09-09'),
        (17, 'Quinn Harris', 5, 'Pune', 92000, '2018-02-17'),
        (18, 'Rita Singh', 3, 'Bangalore', 97000, '2024-01-05'),
        (19, 'Sam Green', 4, 'Delhi', 89000, '2022-11-11'),
        (20, 'Tina Zhao', 1, 'Bangalore', 140000, '2015-12-12'),
    ]
    cur.executemany('INSERT OR IGNORE INTO employees VALUES (?,?,?,?,?,?)', employees)

    projects = [
        (1, 'Project Apollo', 500000),
        (2, 'Project Hermes', 250000),
        (3, 'Project Athena', 150000),
        (4, 'Project Zeus', 750000),
        (5, 'Project Hera', 300000),
        (6, 'Project Poseidon', 200000),
        (7, 'Project Ares', 100000),
        (8, 'Project Demeter', 120000),
        (9, 'Project Artemis', 180000),
        (10, 'Project Hephaestus', 220000),
    ]
    cur.executemany('INSERT OR IGNORE INTO projects VALUES (?,?,?)', projects)

    employee_projects = [
        (1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 1), (8, 6), (9, 4), (10, 2),
        (11, 7), (12, 8), (13, 9), (14, 10), (15, 3), (16, 1), (17, 5), (18, 9), (19, 6), (20, 1),
    ]
    cur.executemany('INSERT OR IGNORE INTO employee_projects VALUES (?,?)', employee_projects)

    conn.commit()


def main(force: bool = False):
    if os.path.exists(DB_PATH) and not force:
        print(f"Database {DB_PATH} already exists. Use --force to recreate.")
        return
    if os.path.exists(DB_PATH) and force:
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    seed_sample_data(conn)
    conn.close()
    print(f"Created database at {DB_PATH}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Delete existing DB and recreate")
    args = parser.parse_args()
    main(force=args.force)
