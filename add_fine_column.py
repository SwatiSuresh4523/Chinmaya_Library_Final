import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE issued_books ADD COLUMN fine INTEGER DEFAULT 0")
    print("✅ 'fine' column added to issued_books.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Error or already exists: {e}")

conn.commit()
conn.close()
