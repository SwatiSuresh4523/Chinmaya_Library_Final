import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(returns)")
columns = [col[1] for col in cur.fetchall()]

if "issue_id" not in columns:
    cur.execute("ALTER TABLE returns ADD COLUMN issue_id INTEGER")
    print("✅ issue_id column added to returns table.")
else:
    print("✅ issue_id column already exists.")

conn.commit()
conn.close()
