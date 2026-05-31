import sqlite3
import os

db_path = os.path.join('instance', 'shuttergallery.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
try:
    c.execute("ALTER TABLE user ADD COLUMN reset_code VARCHAR(64)")
    print("reset_code added")
except Exception as e:
    print(f"Error reset_code: {e}")

try:
    c.execute("ALTER TABLE user ADD COLUMN reset_expiration DATETIME")
    print("reset_expiration added")
except Exception as e:
    print(f"Error reset_expiration: {e}")

conn.commit()
conn.close()
