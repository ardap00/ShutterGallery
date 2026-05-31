import os
import glob

templates_dir = r"C:\Users\ardap\.gemini\antigravity\scratch\ShutterGallery\app\templates"

# Delete gallery.html
gallery_html = os.path.join(templates_dir, "main", "gallery.html")
if os.path.exists(gallery_html):
    os.remove(gallery_html)
    print(f"Deleted {gallery_html}")

# Remove gallery link from all html files
html_files = glob.glob(os.path.join(templates_dir, "**", "*.html"), recursive=True)

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    new_lines = []
    modified = False
    for line in lines:
        if "url_for('main.gallery')" in line:
            modified = True
            continue
        new_lines.append(line)
        
    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"Updated {file_path}")
