import sqlite3
c = sqlite3.connect('instance/shuttergallery.db')
tables = c.execute('SELECT name FROM sqlite_master WHERE type="table"').fetchall()
with open('tables_output.txt', 'w') as f:
    f.write(str(tables))
