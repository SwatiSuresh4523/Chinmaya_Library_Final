import sqlite3

conn = sqlite3.connect("library.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Try each likely table to find where 'fine' is missing
tables = ["issued_books", "transactions", "history", "issue_return"]

for table in tables:
    try:
        print(f"\n🔍 Checking table: {table}")
        cur.execute(f"SELECT * FROM {table} LIMIT 1")
        row = cur.fetchone()
        if row:
            print("✅ Fields:", list(dict(row).keys()))
        else:
            print("⚠️ Table exists but no data.")
    except Exception as e:
        print(f"❌ Error with {table}: {e}")

conn.close()
