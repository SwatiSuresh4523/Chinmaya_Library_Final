import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Create students table
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_no TEXT,
    photo_url TEXT,
    name TEXT,
    class TEXT,
    books_issued INTEGER,
    active INTEGER,
    created_at TEXT
)
""")

# Create teachers table
cur.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_no TEXT,
    photo_url TEXT,
    name TEXT,
    subject TEXT,
    books_issued INTEGER,
    active INTEGER,
    created_at TEXT
)
""")

# Create issues table
cur.execute("""
CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_no TEXT,
    book_id TEXT,
    due_date TEXT,
    return_date TEXT
)
""")

# Create returns table
cur.execute("""
CREATE TABLE IF NOT EXISTS returns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_no TEXT,
    book_id TEXT,
    return_date TEXT,
    fine_collected REAL
)
""")

conn.commit()
conn.close()
print("✅ library.db created with all tables.")
