import sqlite3

DB_PATH = "library.db"  # Update if your DB is in another folder

def add_column_if_not_exists(table_name, column_name, column_type):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cur.fetchall()]

        if column_name not in columns:
            cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            print(f"✅ '{column_name}' column added to '{table_name}' table.")
        else:
            print(f"ℹ️ Column '{column_name}' already exists in '{table_name}'.")

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"❌ Error adding column '{column_name}' to '{table_name}':", e)

def run_all_fixes():
    # Books table fixes
    add_column_if_not_exists("books", "added_on", "TEXT")

    # Users table fixes
    add_column_if_not_exists("users", "class_group", "TEXT")
    add_column_if_not_exists("users", "section", "TEXT")
    add_column_if_not_exists("users", "group_name", "TEXT")
    add_column_if_not_exists("users", "status", "TEXT")
    add_column_if_not_exists("users", "phone_number", "TEXT")
    add_column_if_not_exists("users", "account_type", "TEXT")

run_all_fixes()
