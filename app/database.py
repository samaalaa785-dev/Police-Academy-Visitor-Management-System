import sqlite3
import pandas as pd
from datetime import datetime

DB_PATH = "academy_visitors.db"

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        national_id TEXT,
        phone TEXT,
        reason TEXT,
        submitted_at TEXT
    )""")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        national_id TEXT,
        phone TEXT,
        role TEXT,
        permissions TEXT
    )""")
    con.commit()
    con.close()

def insert_visitor(name, national_id, phone, reason):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    now = datetime.utcnow().isoformat()
    cur.execute("INSERT INTO visitors (name,national_id,phone,reason,submitted_at) VALUES (?,?,?,?,?)",
                (name, national_id, phone, reason, now))
    con.commit()
    con.close()

def query_visitors(search=None):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    if search:
        like = f"%{search}%"
        cur.execute("SELECT id,name,national_id,phone,reason,submitted_at FROM visitors WHERE name LIKE ? OR national_id LIKE ?",
                    (like, like))
    else:
        cur.execute("SELECT id,name,national_id,phone,reason,submitted_at FROM visitors ORDER BY submitted_at DESC")
    rows = cur.fetchall()
    con.close()
    return rows

def export_visitors_to_excel(path):
    rows = query_visitors()
    df = pd.DataFrame(rows, columns=["id","name","national_id","phone","reason","submitted_at"])
    df.to_excel(path, index=False)

