import sqlite3

# Connect to the library database
conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Check all columns in the 'students' table
cur.execute("PRAGMA table_info(students)")
columns = [col[1] for col in cur.fetchall()]

# Define the required columns and their types
required_columns = {
    "account_no": "TEXT",
    "name": "TEXT",
    "roll_no": "TEXT",
    "class": "TEXT",
    "contact": "TEXT",
    "photo_url": "TEXT",
    "admission_date": "TEXT",
    "active": "INTEGER",
    "books_issued": "INTEGER",
    "created_at": "TEXT"
}

# Loop through and add missing columns
for col, col_type in required_columns.items():
    if col not in columns:
        cur.execute(f"ALTER TABLE students ADD COLUMN {col} {col_type}")
        print(f"✅ Added missing column: {col}")

conn.commit()
conn.close()
print("✅ All required columns are now in the 'students' table.")
import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Add 'active' column if it doesn't exist
cur.execute("PRAGMA table_info(students)")
columns = [col[1] for col in cur.fetchall()]
if "active" not in columns:
    cur.execute("ALTER TABLE students ADD COLUMN active INTEGER DEFAULT 1")
    print("✅ 'active' column added.")
else:
    print("✅ 'active' column already exists.")

conn.commit()
conn.close()
