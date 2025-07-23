import sqlite3

DB_PATH = "library.db"  # Path to your database

def check_columns():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("\n📋 Checking columns in 'issued_books' table:")
    cur.execute("PRAGMA table_info(issued_books)")
    for col in cur.fetchall():
        print(col)

    conn.close()

def insert_test_issue():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    accession_no = "B123"
    student_name = "Test Student"
    user_id = "STU123"
    issue_date = "2025-07-15"
    due_date = "2025-07-22"

    print("\n➕ Inserting test issued book...")
    cur.execute("""
    INSERT INTO issued_books (accession_no, student_name, user_id, issue_date, due_date)
    VALUES (?, ?, ?, ?, ?)
    """, (accession_no, student_name, user_id, issue_date, due_date))

    conn.commit()
    conn.close()
    print("✅ Test issue inserted successfully!")

def view_recent_issues():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("\n📄 Recent issued books:")
    cur.execute("SELECT * FROM issued_books ORDER BY id DESC LIMIT 5")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    conn.close()

# Run all steps
check_columns()
insert_test_issue()
view_recent_issues()
