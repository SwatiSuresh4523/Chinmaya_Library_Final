import sqlite3

DB_PATH = "library.db"

# Connect to the database
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Function to check if a column exists in a table
def column_exists(table, column):
    cur.execute(f"PRAGMA table_info({table})")
    return column in [row[1] for row in cur.fetchall()]

# Columns to ensure in 'teachers' table
required_columns = {
    "contact": "TEXT",
    "joining_date": "TEXT",
    "photo_url": "TEXT",
    "active": "INTEGER DEFAULT 1",
    "books_issued": "INTEGER DEFAULT 0",
    "created_at": "TEXT"
}

for column, col_type in required_columns.items():
    if not column_exists("teachers", column):
        cur.execute(f"ALTER TABLE teachers ADD COLUMN {column} {col_type}")
        print(f"✅ Added column '{column}' to 'teachers' table.")

conn.commit()
conn.close()
print("🎉 All missing columns have been added to 'teachers' table.")

