import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'shuttergallery.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='followers'")
    if not cursor.fetchone():
        print("Creating followers table...")
        cursor.execute('''
            CREATE TABLE followers (
                follower_id INTEGER,
                followed_id INTEGER,
                FOREIGN KEY(follower_id) REFERENCES users(id),
                FOREIGN KEY(followed_id) REFERENCES users(id)
            )
        ''')
        conn.commit()
        print("Followers table created successfully.")
    else:
        print("Followers table already exists.")
        
    conn.close()

if __name__ == '__main__':
    migrate()
