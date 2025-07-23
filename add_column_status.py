import sqlite3

# Path to your library.db file
DB_PATH = "library.db"

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Try adding the 'status' column to the 'books' table
try:
    cursor.execute("ALTER TABLE books ADD COLUMN status TEXT DEFAULT 'Available'")
    print("✅ Column 'status' added to 'books' table.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Skipped: {e}")

# Commit and close the connection
conn.commit()
conn.close()
