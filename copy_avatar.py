import shutil
import sys

source = r'C:\Users\ardap\.gemini\antigravity\brain\9e69f0bf-73d2-46d7-926c-4fdbec910a22\media__1780218028944.png'
dest = r'C:\Users\ardap\.gemini\antigravity\scratch\ShutterGallery\app\static\avatars\default.jpg'

try:
    shutil.copyfile(source, dest)
    print("Avatar copied successfully.")
except Exception as e:
    print(f"Error copying avatar: {e}")
