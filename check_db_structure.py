import sqlite3

# Connect to your database file
conn = sqlite3.connect("library.db")  # Make sure this file exists in the same folder
cur = conn.cursor()

# Show structure of 'books' table
print("\n--- Books Table ---")
cur.execute("PRAGMA table_info(books)")
for row in cur.fetchall():
    print(row)

# Show structure of 'issues' table
print("\n--- Issues Table ---")
cur.execute("PRAGMA table_info(issues)")
for row in cur.fetchall():
    print(row)

# Show structure of 'students' table
print("\n--- Students Table ---")
cur.execute("PRAGMA table_info(students)")
for row in cur.fetchall():
    print(row)

# Done
conn.close()
