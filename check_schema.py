import sqlite3

try:
    conn = sqlite3.connect('instance/shuttergallery.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    print(cursor.fetchall())
    
    cursor.execute("SELECT id, username, unique_id FROM users")
    print(cursor.fetchall())
except Exception as e:
    print(f"Error: {e}")
