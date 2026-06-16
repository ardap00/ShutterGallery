import shutil
import os

db_path = os.path.join('instance', 'shuttergallery.db')
bak_path = os.path.join('instance', 'shuttergallery.db.bak')

if os.path.exists(bak_path):
    print(f"Restoring {bak_path} to {db_path}...")
    shutil.copy2(bak_path, db_path)
    print("Restore complete.")
else:
    print(f"Backup file not found at {bak_path}")
