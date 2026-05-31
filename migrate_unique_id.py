import os
import uuid
import sqlite3
from run import app
from app import db
from app.models import User

def migrate():
    db_path = os.path.join(app.instance_path, 'shuttergallery.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if unique_id column exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'unique_id' not in columns:
        print("Adding unique_id column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN unique_id VARCHAR(8)")
        conn.commit()
    
    conn.close()
    
    # Generate unique IDs for existing users using SQLAlchemy context
    with app.app_context():
        users = User.query.all()
        for user in users:
            if not user.unique_id:
                uid = str(uuid.uuid4())[:6].upper()
                while User.query.filter_by(unique_id=uid).first():
                    uid = str(uuid.uuid4())[:6].upper()
                user.unique_id = uid
                print(f"Generated ID #{uid} for user {user.username}")
        db.session.commit()
        print("Migration complete.")

if __name__ == '__main__':
    migrate()
