import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Create transactions table
cur.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id TEXT,
    book_title TEXT,
    user_id TEXT,
    user_name TEXT,
    issue_date TEXT,
    due_date TEXT,
    return_date TEXT,
    fine INTEGER
)
""")

print("✅ Table 'transactions' created successfully!")

conn.commit()
conn.close()
