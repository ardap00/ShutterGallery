import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'instance', 'shuttergallery.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE users ADD COLUMN language VARCHAR(2) NOT NULL DEFAULT 'tr'")
    conn.commit()
    print("Column added successfully.")
except sqlite3.OperationalError as e:
    print(f"Error: {e}")
conn.close()
