import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE issue_return ADD COLUMN status TEXT")
    print("✅ 'status' column added successfully.")
except sqlite3.OperationalError as e:
    print("⚠️ Error:", e)

conn.commit()
conn.close()
