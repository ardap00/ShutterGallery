import os
from PIL import Image
import shutil

source_image = r"C:\Users\ardap\.gemini\antigravity-ide\brain\fe31b069-8d90-4e1d-8042-afdb55701f33\shutter_gallery_icon_1781597956063.png"
dest_dir = r"c:\Users\ardap\.gemini\antigravity\scratch\ShutterGallery\app\static\icons"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

try:
    with Image.open(source_image) as img:
        img_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
        img_192.save(os.path.join(dest_dir, "icon-192.png"))
        
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        img_512.save(os.path.join(dest_dir, "icon-512.png"))
        
    print("Icons successfully created!")
except Exception as e:
    print(f"Error: {e}")
