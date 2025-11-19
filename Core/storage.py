import sqlite3
from datetime import datetime
from Core.models import Task

DB = "data/tasks.db"




def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                note TEXT,
                due TEXT, 
                duration INTEGER,
                keep INTEGER,
                calender_event_id TEXT,
                keep_note_id TEXT,
                google_task_id TEXT

            )
        

""")
    conn.commit()
    conn.close()

def migrate_db():
    conn = sqlite3.connect("data/tasks.db")
    c = conn.cursor()

    # Check if google_task_id column exists
    c.execute("PRAGMA table_info(tasks);")
    columns = [col[1] for col in c.fetchall()]

    if "google_task_id" not in columns:
        print("Migrating DB: Adding google_task_id column...")
        c.execute("ALTER TABLE tasks ADD COLUMN google_task_id TEXT;")
        conn.commit()

    conn.close()

migrate_db()

def addTask(title, note="", due=None, duration=None, keep=False):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
            INSERT INTO tasks (title, note, due, duration, keep)
            VALUES (?, ?, ?, ?, ?)
                """, (title, note, due, duration, int(keep)))
    conn.commit()
    tid = cur.lastrowid
    conn.close()
    return tid

def get_tasks():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    rows = cur.execute("SELECT * FROM TASKS").fetchall()
    conn.close()

    tasks = []
    for r in rows:
        tasks.append(Task(
            id=r[0],
            title=r[1],
            note=r[2],
            due=datetime.fromisoformat(r[3]) if r[3] else None,
            duration = r[4],
            keep=bool(r[5]),
            calender_event_id=r[6],
            keep_note_id=r[7],
            google_task_id=r[8]
        ))
    return tasks

def get_task(task_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    row = cur.execute("SELECT * FROM TASKS WHERE id=?", (task_id,)).fetchone()
    conn.close()

    if not row:
        return None
    return Task(
        id=row[0],
        title=row[1],
        note=row[2],
        due=datetime.fromisoformat(row[3]) if row[3] else None,
        duration=row[4],
        keep=bool(row[5]),
        calender_event_id=row[6],
        keep_note_id=row[7],
        google_task_id=row[8]
    )    
def update_calender_event(task_id, event_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET calender_event_id=? WHERE id=?", (event_id, task_id))
    conn.commit()
    conn.close()

def update_keep_note(task_id, note_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET keep_note_id=? WHERE id=?", (note_id, task_id))
    conn.commit()
    conn.close()

def update_google_task_id(task_id, google_task_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET google_task_id=? WHERE id=?", (google_task_id, task_id))
    conn.commit()
    conn.close()

def mark_done(task_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    cur.close()

def save_calendar_event(title, note, due, duration, event_id, keep=False):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (title, note, due, duration, keep, calender_event_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, note, due, duration, int(keep), event_id))

    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

