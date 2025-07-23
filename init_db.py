import sqlite3

def init_db():
    conn = sqlite3.connect("library.db")
    cur = conn.cursor()

    # ✅ Create or update books table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS books (
        accession_no TEXT PRIMARY KEY,
        title TEXT,
        author TEXT,
        publisher TEXT,
        year TEXT,
        category TEXT,
        added_on TEXT DEFAULT (DATE('now'))
    )
    """)
    print("✅ 'books' table ensured.")

    # ✅ Create issued_books table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS issued_books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        accession_no TEXT,
        student_name TEXT,
        user_id TEXT,
        issue_date TEXT,
        due_date TEXT,
        return_date TEXT,
        fine INTEGER DEFAULT 0
    )
    """)
    print("✅ 'issued_books' table ensured.")

    # ✅ Add 'available' column if not exists
    cur.execute("PRAGMA table_info(books);")
    book_columns = [col[1] for col in cur.fetchall()]
    if 'available' not in book_columns:
        cur.execute("ALTER TABLE books ADD COLUMN available INTEGER DEFAULT 1")
        print("🆕 'available' column added to books table.")
    else:
        print("✅ 'available' column already exists in books.")

    # ✅ Create students table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        account_no TEXT PRIMARY KEY,
        name TEXT,
        class TEXT,
        phone TEXT
    )
    """)
    print("✅ 'students' table ensured.")

    # ✅ Create teachers table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        account_no TEXT PRIMARY KEY,
        name TEXT,
        subject TEXT,
        phone TEXT
    )
    """)
    print("✅ 'teachers' table ensured.")

    # ✅ Create ask_librarian table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ask_librarian (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        account_no TEXT,
        message TEXT,
        filename TEXT,
        date TEXT DEFAULT (DATETIME('now')),
        status TEXT DEFAULT 'Pending'
    )
    """)
    print("✅ 'ask_librarian' table ensured.")

    # ✅ Create or update users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT
    )
    """)
    print("✅ 'users' table ensured.")

    # ✅ Check and add columns to users
    cur.execute("PRAGMA table_info(users);")
    user_columns = [col[1] for col in cur.fetchall()]
    print("✅ Existing columns in users:", user_columns)

    for col in ["username", "email", "phone", "account_type", "password"]:
        if col not in user_columns:
            cur.execute(f"ALTER TABLE users ADD COLUMN {col} TEXT;")
            print(f"🆕 '{col}' column added to users.")
        else:
            print(f"✅ '{col}' already exists in users.")

    # ✅ Create issue_return_history table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS issue_return_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        user_id INTEGER,
        user_type TEXT,
        issue_date TEXT,
        return_date TEXT,
        remarks TEXT
    )
    """)
    print("✅ 'issue_return_history' table ensured.")

    conn.commit()
    conn.close()
    print("✅ All database tables and columns initialized successfully.")

import sqlite3

conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Add password column if it doesn't exist
cursor.execute("PRAGMA table_info(users)")
columns = [col[1] for col in cursor.fetchall()]
if 'password' not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")
    print("✅ 'password' column added.")
else:
    print("ℹ️ 'password' column already exists.")

conn.commit()
conn.close()

import sqlite3

conn = sqlite3.connect("library.db")  # Change if your DB has a different name
cursor = conn.cursor()

# Add the category column if it doesn't exist
try:
    cursor.execute("ALTER TABLE gallery_images ADD COLUMN category TEXT;")
    print("✅ 'category' column added successfully.")
except Exception as e:
    print("⚠️ Error:", e)

conn.commit()
conn.close()

import sqlite3

DB_PATH = 'library.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        # ✅ Create the users table if it doesn't exist
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT
        )
        """)

        # ✅ Check and add missing columns
        cur.execute("PRAGMA table_info(users);")
        existing_columns = [col[1] for col in cur.fetchall()]
        
        required_columns = {
            "username": "TEXT",
            "email": "TEXT",
            "phone": "TEXT",
            "class_or_group": "TEXT",
            "gender": "TEXT",
            "join_date": "TEXT",
            "books_borrowed": "INTEGER DEFAULT 0",
            "last_activity": "TEXT",
            "password": "TEXT",
            "account_type": "TEXT"
        }

        for column, definition in required_columns.items():
            if column not in existing_columns:
                cur.execute(f"ALTER TABLE users ADD COLUMN {column} {definition}")
                print(f"✅ Added missing column: {column}")

        conn.commit()
        print("✅ Database initialized and patched successfully.")

# Add missing 'accession_no' column if not exists
def add_missing_columns():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Check if accession_no column exists
        cursor.execute("PRAGMA table_info(books);")
        columns = [col[1] for col in cursor.fetchall()]
        if 'accession_no' not in columns:
            cursor.execute("ALTER TABLE books ADD COLUMN accession_no TEXT;")
        conn.commit()

# Call this after init_db()
init_db()
add_missing_columns()


# Run it
if __name__ == "__main__":
    init_db()
