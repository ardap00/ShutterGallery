import sqlite3
import traceback

with open("db_schema_output.txt", "w") as f:
    try:
        conn = sqlite3.connect('instance/shuttergallery.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        cols = cursor.fetchall()
        f.write(f"Columns: {cols}\n")
    except Exception as e:
        f.write(f"Error: {traceback.format_exc()}\n")
