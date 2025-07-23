import sqlite3
from datetime import datetime

DB_PATH = "library.db"

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 📚 Books Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            accession TEXT,
            isbn TEXT,
            title TEXT,
            author TEXT,
            publisher TEXT,
            year TEXT,
            category TEXT,
            status TEXT DEFAULT 'Available',
            available INTEGER DEFAULT 1,
            added_on TEXT DEFAULT (DATE('now'))
        )
    """)

    # 👩‍🎓 Students Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            account_no TEXT PRIMARY KEY,
            name TEXT,
            roll_no TEXT,
            class TEXT,
            section TEXT,
            contact TEXT,
            photo_url TEXT,
            admission_date TEXT,
            active INTEGER DEFAULT 1,
            books_issued INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    # 👨‍🏫 Teachers Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            account_no TEXT PRIMARY KEY,
            name TEXT,
            subject TEXT,
            contact TEXT,
            photo_url TEXT,
            joining_date TEXT,
            active INTEGER DEFAULT 1,
            books_issued INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    # 📄 Issues Table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS issues (
            issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_no TEXT,
            book_id INTEGER,
            user_type TEXT DEFAULT 'student',
            issue_date TEXT,
            due_date TEXT,
            return_date TEXT,
            fine_collected INTEGER DEFAULT 0
        )
    """)

    # 📦 Returns Table (used for history/logs)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS returns (
            return_id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_id INTEGER,
            account_no TEXT,
            book_id INTEGER,
            return_date TEXT,
            fine_collected INTEGER
        )
    """)

    # 🧾 Transactions (optional unified table for dashboard stats)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            user_id TEXT,
            issue_date TEXT,
            due_date TEXT,
            return_date TEXT,
            fine INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()
    print("✅ All necessary tables are created or verified.")

if __name__ == "__main__":
    create_tables()
