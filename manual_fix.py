import os
import re

def fix():
    files_to_fix = []
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app', 'templates'))
    for root, dirs, files in os.walk(base):
        for f in files:
            if f.endswith('.html'):
                files_to_fix.append(os.path.join(root, f))
    
    for path in files_to_fix:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        old_content = content
        
        # Replace the green
        content = re.sub(r'emerald-\d00', '[#829A73]', content)
        content = re.sub(r'16,\s*185,\s*129', '130,154,115', content)
        
        # Replace the background
        content = re.sub(
            r"url\('https://images\.unsplash\.com/photo-1536924940846-227afb31e2a5.*?'\)",
            "url('https://images.unsplash.com/photo-1577720580479-7d839d829c73?q=80&w=1920')",
            content
        )
        content = content.replace('filter: blur(28px) brightness(30%);', 'filter: blur(4px) brightness(20%);')
        
        if content != old_content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {path}")
            
if __name__ == '__main__':
    fix()
