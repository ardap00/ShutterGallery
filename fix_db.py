import sqlite3
import os

db_path = os.path.join('instance', 'shuttergallery.db')
if not os.path.exists(db_path):
    print("DB not found at", db_path)
else:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute("ALTER TABLE users ADD COLUMN bio VARCHAR(200)")
        print("Added bio")
    except sqlite3.OperationalError as e:
        print("Bio error:", e)
        
    try:
        c.execute("ALTER TABLE users ADD COLUMN avatar_file VARCHAR(256) DEFAULT 'default.jpg'")
        print("Added avatar_file")
    except sqlite3.OperationalError as e:
        print("Avatar error:", e)
        
    # Also we should update existing rows to have default.jpg
    c.execute("UPDATE users SET avatar_file = 'default.jpg' WHERE avatar_file IS NULL")
        
    conn.commit()
    conn.close()
    print("Done")
