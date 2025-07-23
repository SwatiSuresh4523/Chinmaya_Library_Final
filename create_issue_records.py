import sqlite3

DB_PATH = "library.db"

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    # Create issue_records table with all required columns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issue_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            book_id TEXT,
            book_title TEXT,
            issue_date TEXT,
            return_date TEXT,
            fine REAL
        )
    ''')

    print("✅ issue_records table created or already exists.")
