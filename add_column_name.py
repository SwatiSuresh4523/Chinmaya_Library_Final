import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Add to students
try:
    cur.execute("ALTER TABLE students ADD COLUMN name TEXT")
    print("✅ Added 'name' column to students")
except:
    print("⚠️ 'name' already exists in students")

# Add to teachers
try:
    cur.execute("ALTER TABLE teachers ADD COLUMN name TEXT")
    print("✅ Added 'name' column to teachers")
except:
    print("⚠️ 'name' already exists in teachers")

# Add to issue_return
try:
    cur.execute("ALTER TABLE issue_return ADD COLUMN name TEXT")
    print("✅ Added 'name' column to issue_return")
except:
    print("⚠️ 'name' already exists in issue_return")

conn.commit()
conn.close()
