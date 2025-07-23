import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Check if section column already exists
cur.execute("PRAGMA table_info(students)")
columns = [col[1] for col in cur.fetchall()]

if "section" not in columns:
    cur.execute("ALTER TABLE students ADD COLUMN section TEXT DEFAULT 'A'")
    print("✅ 'section' column added to students table.")
else:
    print("ℹ️ 'section' column already exists.")

conn.commit()
conn.close()
