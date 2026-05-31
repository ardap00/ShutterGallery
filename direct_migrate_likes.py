import sqlite3
import os

db_path = os.path.join('instance', 'shuttergallery.db')
conn = sqlite3.connect(db_path)
conn.execute('''
    CREATE TABLE IF NOT EXISTS likes (
        user_id INTEGER,
        post_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(post_id) REFERENCES photo_posts(id)
    )
''')
conn.commit()
print("Likes table created successfully.")
