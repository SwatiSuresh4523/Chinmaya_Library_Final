import sqlite3

# Required new columns
required_columns = {
    "accession": "TEXT",
    "isbn": "TEXT",
    "status": "TEXT DEFAULT 'available'"
}

# Connect to the SQLite database
conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Step 1: Get existing columns
cur.execute("PRAGMA table_info(books)")
existing_columns = [col[1] for col in cur.fetchall()]

# Step 2: Add missing columns
for col_name, col_type in required_columns.items():
    if col_name not in existing_columns:
        try:
            cur.execute(f"ALTER TABLE books ADD COLUMN {col_name} {col_type}")
            print(f"✅ Added missing column: {col_name} ({col_type})")
        except sqlite3.OperationalError as e:
            print(f"❌ Error adding {col_name}: {e}")
    else:
        print(f"✅ Column already exists: {col_name}")

# Save changes and close
conn.commit()
conn.close()
print("✅ All checks complete.")
