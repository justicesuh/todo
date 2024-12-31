import sqlite3
from pathlib import Path
from typing import Any


def get_connection(path: Path):
    return sqlite3.connect(path)


def create_db(path: Path, name: str):
    db_path = path / f'{name}.db'
    if db_path.exists():
        return

    conn = get_connection(db_path)
    cursor = conn.cursor()

    cursor.execute('PRAGMA foreign_keys = ON;')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        color INTEGER,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS labels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        color INTEGER,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        name TEXT NOT NULL,
        description TEXT,
        is_completed INTEGER DEFAULT 0,
        is_deleted INTEGER DEFAULT 0,
        start_date TEXT,
        deadline TEXT,
        duration INTEGER,
        frequency INTEGER,
        day_of_week INTEGER,
        day_of_month INTEGER,
        recurrence_date TEXT,
        priority INTEGER,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS task_labels (
        task_id INTEGER NOT NULL,
        label_id INTEGER NOT NULL,
        PRIMARY KEY (task_id, label_id),
        FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
        FOREIGN KEY (label_id) REFERENCES labels(id) ON DELETE CASCADE
    );
    ''')

    conn.commit()
    conn.close()


class DB:
    def __init__(self, path: Path):
        self.path = path

    def execute_query(self, query: str, params: list[Any] = []):
        with get_connection(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    def fetch_all(self, query: str, params: list[Any] = []):
        with get_connection(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
        
    def fetch_one(self, query: str, params: list[Any] = []):
        with get_connection(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
