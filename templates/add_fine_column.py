import sqlite3

DB_PATH = "library.db"  # adjust if needed
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE issued_books ADD COLUMN fine INTEGER DEFAULT 0")
    print("✅ 'fine' column added to issued_books table.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Error or already exists: {e}")

conn.commit()
conn.close()
