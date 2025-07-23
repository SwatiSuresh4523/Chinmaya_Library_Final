import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(returns)")
columns = [col[1] for col in cur.fetchall()]

print("📋 Columns in 'returns' table:")
for col in columns:
    print("-", col)

conn.close()
