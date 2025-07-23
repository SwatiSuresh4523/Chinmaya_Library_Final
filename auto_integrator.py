# Chinmaya Smart Library - Full Auto Integration Script
# Detects and processes new files (Excel, CSV, HTML) in auto_import folder

import os
import sqlite3
import pandas as pd
from datetime import datetime

# Configuration
DB_PATH = "library.db"
IMPORT_FOLDER = "auto_import"
os.makedirs(IMPORT_FOLDER, exist_ok=True)

# Connect to DB
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Helper function: validate required columns
def validate_columns(df, required_cols):
    return required_cols.issubset(set(df.columns))

# Book table structure
book_columns = {"id", "title", "author", "publisher", "category", "publication_year", "status"}

print("📂 Scanning for files in 'auto_import' folder...")

for filename in os.listdir(IMPORT_FOLDER):
    filepath = os.path.join(IMPORT_FOLDER, filename)

    if filename.endswith(".xlsx") or filename.endswith(".csv"):
        print(f"🔍 Processing: {filename}")
        try:
            if filename.endswith(".xlsx"):
                df = pd.read_excel(filepath)
            else:
                df = pd.read_csv(filepath)

            if validate_columns(df, book_columns):
                df.to_sql("books", conn, if_exists="append", index=False)
                print("✅ Book catalog imported into database.")
            else:
                print("⚠️ Skipped. Columns do not match expected format for books table.")

        except Exception as e:
            print(f"❌ Failed to import {filename}: {e}")

    elif filename.endswith(".html"):
        print(f"📄 Detected HTML file: {filename}. Please move it manually to the templates/ folder.")

    elif filename.endswith(".db"):
        print(f"🗃️ Skipping DB file: {filename}. Manual merge required for database integrity.")

    else:
        print(f"⛔ Unsupported file type: {filename}. Skipped.")

conn.close()
print("✅ Auto integration completed. Clean and synced.")
