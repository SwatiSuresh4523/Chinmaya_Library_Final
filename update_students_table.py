import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(students)")
columns = [col[1] for col in cur.fetchall()]

required = {
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

for col, col_type in required.items():
    if col not in columns:
        cur.execute(f"ALTER TABLE students ADD COLUMN {col} {col_type}")
        print(f"✅ Added: {col}")

conn.commit()
conn.close()
