import os

directory = r'C:\Users\ardap\.gemini\antigravity\scratch\ShutterGallery\app\templates'
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if 'image_file' in content or 'avatar_file' in content or 'avatar_url' in content or 'filename=' in content:
                print(filepath)
