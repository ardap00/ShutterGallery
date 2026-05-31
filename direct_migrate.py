import sqlite3
import os

db_path = os.path.join('instance', 'shuttergallery.db')
conn = sqlite3.connect(db_path)
conn.execute('''
    CREATE TABLE IF NOT EXISTS followers (
        follower_id INTEGER,
        followed_id INTEGER,
        FOREIGN KEY(follower_id) REFERENCES users(id),
        FOREIGN KEY(followed_id) REFERENCES users(id)
    )
''')
conn.commit()
print("Direct SQLite create table successful.")
