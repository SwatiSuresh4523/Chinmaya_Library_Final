import sqlite3

# Connect to your library database
conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Show all columns in the 'issue_return' table
cur.execute("PRAGMA table_info(issue_return)")
columns = cur.fetchall()

print("📋 Columns in 'issue_return' table:")
for col in columns:
    print(f"- {col[1]} (type: {col[2]})")

conn.close()
