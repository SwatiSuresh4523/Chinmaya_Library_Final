import sqlite3

conn = sqlite3.connect("library.db")  # Make sure this path is correct
cur = conn.cursor()

print("📚 Books Table Columns:")
cur.execute("PRAGMA table_info(books)")
print(cur.fetchall())

print("\n👤 Students Table Columns:")
cur.execute("PRAGMA table_info(students)")
print(cur.fetchall())

print("\n🔁 Issues Table Columns:")
cur.execute("PRAGMA table_info(issues)")
print(cur.fetchall())

conn.close()
