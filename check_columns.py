import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

print("📋 Columns in 'students' table:")
cur.execute("PRAGMA table_info(students)")
for col in cur.fetchall():
    print(f"- {col[1]} ({col[2]})")

print("\n📋 Columns in 'teachers' table:")
cur.execute("PRAGMA table_info(teachers)")
for col in cur.fetchall():
    print(f"- {col[1]} ({col[2]})")

conn.close()
