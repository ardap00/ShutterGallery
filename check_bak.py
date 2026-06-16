import sqlite3
import os

db_path = os.path.join('instance', 'shuttergallery.db.bak')
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in {db_path}: {tables}")
    
    if len(tables) > 0:
        for table in tables:
            t = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {t}")
            count = cursor.fetchone()[0]
            print(f"Table {t} has {count} rows.")
else:
    print(f"File not found: {db_path}")
