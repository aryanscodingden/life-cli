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
                keep_note_id TEXT
    
            )
        

""")
    conn.commit()
    conn.close()

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
        ))
    return tasks
    
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

def mark_done(task_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    cur.close()

