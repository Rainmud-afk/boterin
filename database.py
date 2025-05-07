import sqlite3

DB_NAME = "soul_log.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS entries (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        text TEXT
    )""")
    conn.commit()
    conn.close()

def save_entry(user_id, text):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO entries (user_id, text) VALUES (?, ?)", (user_id, text))
    conn.commit()
    conn.close()

def get_entries_by_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM entries WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    entries = cur.fetchall()
    conn.close()
    return entries
