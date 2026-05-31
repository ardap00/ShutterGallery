import os
import re

def main():
    templates = os.path.join(os.path.dirname(__file__), 'app', 'templates')
    log = []
    
    for root, dirs, files in os.walk(templates):
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                new_content = content
                
                # Colors
                new_content = re.sub(r'emerald-\d00', '[#829A73]', new_content)
                new_content = re.sub(r'16,\s*185,\s*129', '130,154,115', new_content)
                
                # Replace the backgrounds
                new_content = re.sub(
                    r"url\('https://images\.unsplash\.com/photo-1536924940846-227afb31e2a5.*?'\)",
                    "url('https://images.unsplash.com/photo-1577720580479-7d839d829c73?q=80&w=1920')",
                    new_content
                )
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    log.append(f"Fixed {f}")
    
    with open('fix_result.txt', 'w') as f:
        f.write('\n'.join(log))

if __name__ == '__main__':
    main()
