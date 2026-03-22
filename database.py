import sqlite3
from datetime import datetime

# 🔗 Connect to SQLite database
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

# 📦 Create tasks table (if not exists)
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    task TEXT NOT NULL,
    created_at TEXT NOT NULL
)
""")
conn.commit()


# ✅ Add Task
def add_task(user_id, task):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO tasks (user_id, task, created_at) VALUES (?, ?, ?)",
        (user_id, task, created_at)
    )
    conn.commit()


# 📋 Get All Tasks for User
def get_tasks(user_id):
    cursor.execute(
        "SELECT id, task, created_at FROM tasks WHERE user_id=? ORDER BY id DESC",
        (user_id,)
    )
    return cursor.fetchall()


# 🗑 Delete Specific Task
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()


# 🧹 Clear All Tasks of User
def clear_tasks(user_id):
    cursor.execute("DELETE FROM tasks WHERE user_id=?", (user_id,))
    conn.commit()


# 📊 Count Tasks
def count_tasks(user_id):
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id=?", (user_id,))
    return cursor.fetchone()[0]


# 🔍 Check if Task Exists (Advanced)
def task_exists(task_id):
    cursor.execute("SELECT 1 FROM tasks WHERE id=?", (task_id,))
    return cursor.fetchone() is not None
