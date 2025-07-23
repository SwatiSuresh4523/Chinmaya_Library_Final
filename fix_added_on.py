import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE books ADD COLUMN added_on TEXT DEFAULT ''")
    print("✅ 'added_on' column added to books table.")
except sqlite3.OperationalError as e:
    print("⚠️ Already exists or error:", e)

conn.commit()
conn.close()
