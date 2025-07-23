import sqlite3

conn = sqlite3.connect('library.db')  # Make sure this matches your actual DB path
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS gallery_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        filename TEXT NOT NULL,
        uploaded_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("✅ gallery_images table created.")
