import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# ✅ Add 'user_role' to 'issue_return' if missing
cur.execute("PRAGMA table_info(issue_return)")
columns = [col[1] for col in cur.fetchall()]

if 'user_role' not in columns:
    cur.execute("ALTER TABLE issue_return ADD COLUMN user_role TEXT")
    print("✅ 'user_role' column added to issue_return table.")
else:
    print("ℹ️ 'user_role' column already exists in issue_return.")

# ✅ Recreate 'issued_books' with correct structure
cur.execute("DROP TABLE IF EXISTS issued_books")
cur.execute("""
CREATE TABLE issued_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    accession_no TEXT,
    student_name TEXT,
    user_id TEXT,
    issue_date TEXT,
    due_date TEXT,
    return_date TEXT,
    fine INTEGER DEFAULT 0
)
""")
print("✅ issued_books table recreated with accession_no column.")

conn.commit()
conn.close()
