import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Add 'role' column to teachers table if not exists
try:
    cur.execute("ALTER TABLE teachers ADD COLUMN role TEXT")
    print("✅ 'role' column added to teachers table.")
except sqlite3.OperationalError as e:
    print("ℹ️", e)

conn.commit()
conn.close()
