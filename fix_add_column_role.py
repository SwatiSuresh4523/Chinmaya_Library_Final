import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Check and add 'role' column to students table if not exists
try:
    cur.execute("ALTER TABLE students ADD COLUMN role TEXT")
    print("✅ 'role' column added to students table.")
except sqlite3.OperationalError as e:
    print("ℹ️", e)

conn.commit()
conn.close()
