import sqlite3
from pathlib import Path


def create_db(path: Path, name: str):
    db_path = path / f'{name}.db'
    if db_path.exists():
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('PRAGMA foreign_keys = ON;')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        color INTEGER,
        created_at TEXT,
        updated_at TEXT
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS labels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        color INTEGER,
        created_at TEXT,
        updated_at TEXT
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
        created_at TEXT,
        updated_at TEXT,
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
