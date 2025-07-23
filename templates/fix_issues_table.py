import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Get all existing column names
cur.execute("PRAGMA table_info(issues)")
existing_columns = [col[1] for col in cur.fetchall()]

# Desired columns and their SQL data types
required_columns = {
    "issue_id": "INTEGER",
    "accession_no": "TEXT",
    "book_title": "TEXT",
    "account_no": "TEXT",
    "name": "TEXT",
    "issue_date": "TEXT",
    "due_date": "TEXT",
    "return_date": "TEXT",
    "status": "TEXT"
}

# Check and add missing columns
for column, col_type in required_columns.items():
    if column not in existing_columns:
        cur.execute(f"ALTER TABLE issues ADD COLUMN {column} {col_type}")
        print(f"✅ Added column: {column} ({col_type})")
    else:
        print(f"✅ Column already exists: {column}")

conn.commit()
conn.close()
print("✅ All column checks complete.")
