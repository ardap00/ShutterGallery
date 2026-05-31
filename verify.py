import sqlite3
import os

db_path = os.path.join('instance', 'shuttergallery.db')
try:
    conn = sqlite3.connect(db_path)
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    with open('verify_output.txt', 'w') as f:
        f.write("Tables in shuttergallery.db: " + str(tables) + "\n")
        
    from app import create_app
    from app.models import db
    app = create_app()
    with app.app_context():
        f.write(f"SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}\n")
except Exception as e:
    with open('verify_output.txt', 'w') as f:
        f.write(str(e))
