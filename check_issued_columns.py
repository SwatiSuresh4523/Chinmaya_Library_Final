import sqlite3

conn = sqlite3.connect("library.db")  # Use your actual DB name
cur = conn.cursor()

cur.execute("PRAGMA table_info(issued_books)")
columns = cur.fetchall()

print("📋 Columns in 'issued_books':")
for col in columns:
    print(f"- {col[1]}")

conn.close()
