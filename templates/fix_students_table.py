import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Check if 'contact' column exists
cur.execute("PRAGMA table_info(students)")
columns = [col[1] for col in cur.fetchall()]

# Add missing columns if not present
missing_columns = []
if "contact" not in columns:
    cur.execute("ALTER TABLE students ADD COLUMN contact TEXT")
    missing_columns.append("contact")
if "created_at" not in columns:
    cur.execute("ALTER TABLE students ADD COLUMN created_at TEXT")
    missing_columns.append("created_at")

if missing_columns:
    print(f"✅ Added columns to students table: {', '.join(missing_columns)}")
else:
    print("✅ All required columns already exist.")

conn.commit()
conn.close()
