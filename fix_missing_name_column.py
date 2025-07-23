import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Add 'name' column to students if missing
try:
    cur.execute("ALTER TABLE students ADD COLUMN name TEXT")
    print("✅ Added 'name' to students")
except:
    print("⚠️ 'name' already exists in students")

# Add 'name' column to teachers if missing
try:
    cur.execute("ALTER TABLE teachers ADD COLUMN name TEXT")
    print("✅ Added 'name' to teachers")
except:
    print("⚠️ 'name' already exists in teachers")

# Add 'name' column to issue_return if missing
try:
    cur.execute("ALTER TABLE issue_return ADD COLUMN name TEXT")
    print("✅ Added 'name' to issue_return")
except:
    print("⚠️ 'name' already exists in issue_return")

conn.commit()
conn.close()
