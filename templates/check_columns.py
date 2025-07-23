import sqlite3

# Connect to your existing database
conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Check the structure of the 'books' table
cur.execute("PRAGMA table_info(books)")
columns = cur.fetchall()

print("📚 Columns in 'books' table:")
for col in columns:
    print(f"- {col[1]} (type: {col[2]})")

conn.close()
