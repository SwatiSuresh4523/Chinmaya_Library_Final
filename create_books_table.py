import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    accession TEXT,
    isbn TEXT,
    title TEXT,
    author TEXT,
    publisher TEXT,
    category TEXT,
    year TEXT,
    status TEXT DEFAULT 'Available',
    added_on TEXT,
    cover_url TEXT
)
""")

conn.commit()
conn.close()

print("✅ New books table created with 'added_on' column.")
