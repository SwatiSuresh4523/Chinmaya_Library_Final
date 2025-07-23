import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

# Add 'title' column if missing
try:
    cur.execute("ALTER TABLE issue_return ADD COLUMN title TEXT")
    print("✅ Added column: title")
except Exception as e:
    print("⚠️ Column 'title' already exists or error:", e)

# Add 'author' column if missing
try:
    cur.execute("ALTER TABLE issue_return ADD COLUMN author TEXT")
    print("✅ Added column: author")
except Exception as e:
    print("⚠️ Column 'author' already exists or error:", e)

conn.commit()
conn.close()
print("🎉 Done updating issue_return table.")
