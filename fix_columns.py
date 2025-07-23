import sqlite3

DB_PATH = "library.db"

def add_column_if_missing(table, column_name, column_type):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Get all existing column names from the table
        cursor.execute(f"PRAGMA table_info({table})")
        existing_columns = [col[1] for col in cursor.fetchall()]

        # If column doesn't exist, add it
        if column_name not in existing_columns:
            try:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column_name} {column_type}")
                print(f"✅ Added column '{column_name}' to '{table}'")
            except Exception as e:
                print(f"⚠️ Failed to add column '{column_name}' to '{table}': {e}")
        else:
            print(f"✅ Column '{column_name}' already exists in '{table}'")

# 🛠 Add required columns to `transactions` table
add_column_if_missing("transactions", "title", "TEXT")
add_column_if_missing("transactions", "author", "TEXT")
add_column_if_missing("transactions", "publisher", "TEXT")
add_column_if_missing("transactions", "isbn", "TEXT")
add_column_if_missing("transactions", "category", "TEXT")

# 🛠 Add required columns to `wishlist` table
add_column_if_missing("wishlist", "status", "TEXT")
add_column_if_missing("wishlist", "reason", "TEXT")
add_column_if_missing("wishlist", "date_requested", "TEXT")

# 🛠 Add required columns to `issue_records` table
add_column_if_missing("issue_records", "book_title", "TEXT")
add_column_if_missing("issue_records", "return_date", "TEXT")
add_column_if_missing("issue_records", "fine", "REAL")

# 🛠 Add required columns to `students` table
add_column_if_missing("students", "contact_number", "TEXT")

# 🛠 Add required columns to `teachers` table
add_column_if_missing("teachers", "subject", "TEXT")

print("\n✅ All column checks complete.\n")
