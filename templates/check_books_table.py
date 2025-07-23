import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(books)")
columns = cur.fetchall()

print("📚 Columns in books table:")
for col in columns:
    print("-", col[1])

conn.close()
