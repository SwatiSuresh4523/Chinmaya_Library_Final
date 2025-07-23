import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# ✅ Add isbn column if it doesn't exist
try:
    cur.execute("ALTER TABLE books ADD COLUMN isbn TEXT")
    print("✅ ISBN column added.")
except Exception as e:
    print("⚠️ Already exists or failed:", e)

conn.commit()
conn.close()
