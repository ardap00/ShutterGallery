import sqlite3
import uuid

# 1. Kolonu ekle
try:
    conn = sqlite3.connect('instance/shuttergallery.db')
    conn.execute("ALTER TABLE users ADD COLUMN unique_id VARCHAR(8)")
    conn.commit()
    print("Column added successfully.")
except sqlite3.OperationalError as e:
    print(f"Error adding column: {e}")

# 2. Var olan kullanıcılara ID ata
try:
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE unique_id IS NULL")
    users = cursor.fetchall()
    
    for (user_id,) in users:
        uid = str(uuid.uuid4())[:6].upper()
        cursor.execute("UPDATE users SET unique_id = ? WHERE id = ?", (uid, user_id))
        print(f"Updated user_id {user_id} with unique_id {uid}")
        
    conn.commit()
    print("IDs generated successfully.")
except Exception as e:
    print(f"Error updating users: {e}")
finally:
    conn.close()
