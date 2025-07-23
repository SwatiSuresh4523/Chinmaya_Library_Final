import sqlite3

# Connect to your database (or create it)
conn = sqlite3.connect("library.db")
cur = conn.cursor()

# -------------------------------
# DROP old tables if needed (optional during reset)
# -------------------------------
cur.execute("DROP TABLE IF EXISTS students")
cur.execute("DROP TABLE IF EXISTS teachers")
cur.execute("DROP TABLE IF EXISTS books")
cur.execute("DROP TABLE IF EXISTS issue_return")

# -------------------------------
# CREATE TABLES
# -------------------------------

# Students table
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_no TEXT UNIQUE,
    name TEXT,
    class TEXT,
    section TEXT,
    contact TEXT,
    created_at TEXT
)
""")

# Teachers table
cur.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_no TEXT UNIQUE,
    name TEXT,
    subject TEXT,
    contact TEXT,
    created_at TEXT
)
""")

# Books table — now includes accession column
cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    accession TEXT UNIQUE,
    book_id TEXT,
    title TEXT,
    author TEXT,
    publisher TEXT,
    category TEXT,
    year TEXT,
    publication TEXT,
    quantity INTEGER
)
""")

# Issue/Return table
cur.execute("""
CREATE TABLE IF NOT EXISTS issue_return (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    user_name TEXT,
    book_id TEXT,
    issue_date TEXT,
    return_date TEXT,
    fine_amount REAL,
    status TEXT,
    user_type TEXT,
    FOREIGN KEY(user_id) REFERENCES students(id)
)
""")

# -------------------------------
# INSERT DUMMY DATA (optional)
# -------------------------------

# Insert sample students
cur.execute("INSERT OR IGNORE INTO students (account_no, name, class, section, contact, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            ("S4523", "Swati Suresh", "10", "A", "9876543210", "2025-07-01"))

# Insert sample teachers
cur.execute("INSERT OR IGNORE INTO teachers (account_no, name, subject, contact, created_at) VALUES (?, ?, ?, ?, ?)",
            ("T101", "Ravi Kumar", "Physics", "9876543211", "2025-07-01"))

# Insert sample books
cur.execute("""
INSERT OR IGNORE INTO books (
    accession, book_id, title, author, publisher, category, year, publication, quantity
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    "B001", "BOOK001", "Wings of Fire", "A.P.J Abdul Kalam", "Penguin", "Biography", "2005", "Penguin India", 5
))

# Insert sample issue
cur.execute("""
INSERT INTO issue_return (
    user_id, user_name, book_id, issue_date, return_date, fine_amount, status, user_type
) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    1, "Swati Suresh", "BOOK001", "2025-07-01", "2025-07-10", 0.0, "Returned", "student"
))

conn.commit()
conn.close()
print("✅ Library database setup completed with all required columns.")
