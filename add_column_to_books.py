import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE books ADD COLUMN added_on TEXT")
    print("✅ 'added_on' column added successfully.")
except sqlite3.OperationalError:
    print("⚠️ Column already exists or error occurred.")

conn.commit()
conn.close()
