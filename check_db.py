import os
import sqlite3

for root, dirs, files in os.walk('.'):
    if 'venv' in root:
        continue
    for file in files:
        if file.endswith('.db'):
            db_path = os.path.join(root, file)
            try:
                conn = sqlite3.connect(db_path)
                tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
                print(f"Database: {db_path} - Tables: {[t[0] for t in tables]}")
            except Exception as e:
                print(f"Failed to read {db_path}: {e}")
