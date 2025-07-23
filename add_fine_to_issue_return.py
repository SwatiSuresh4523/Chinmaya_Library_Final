import sqlite3
import os

db_path = "library.db"  # Change to full path if needed

print("Using DB:", os.path.abspath(db_path))

conn = sqlite3.connect(db_path)
cur = conn.cursor()

try:
    cur.execute("ALTER TABLE issue_return ADD COLUMN fine INTEGER DEFAULT 0")
    print("✅ 'fine' column added to issue_return.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Error or column may already exist: {e}")

conn.commit()
conn.close()
