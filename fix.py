import os
import re

def fix():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'app', 'templates'))
    print(f"Scanning directory: {base_dir}")
    
    count = 0
    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.endswith('.html'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                new_content = content
                
                # Replace backgrounds
                new_content = re.sub(r'bg-emerald-\d00', 'bg-[#829A73]', new_content)
                new_content = re.sub(r'text-emerald-\d00', 'text-[#A3B18A]', new_content)
                new_content = re.sub(r'border-emerald-\d00', 'border-[#A3B18A]', new_content)
                new_content = re.sub(r'shadow-\[0_0_15px_rgba\(16,185,129,0\.4\)\]', 'shadow-[0_0_15px_rgba(163,177,138,0.4)]', new_content)
                new_content = re.sub(r'shadow-\[0_0_25px_rgba\(16,185,129,0\.6\)\]', 'shadow-[0_0_25px_rgba(163,177,138,0.6)]', new_content)
                new_content = re.sub(r'shadow-\[0_0_8px_rgba\(16,185,129,0\.8\)\]', 'shadow-[0_0_8px_rgba(163,177,138,0.8)]', new_content)
                
                # Colors that I injected previously
                new_content = new_content.replace('[#9CA986]', '[#A3B18A]')
                new_content = new_content.replace('[#8B9876]', '[#588157]')
                
                # Images
                new_content = re.sub(r'https://images\.unsplash\.com/photo-1536924940846-227afb31e2a5[^\']+', 'https://images.unsplash.com/photo-1577720580479-7d839d829c73?q=80&w=1920', new_content)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f"Updated {f}")
                    count += 1
                
    print(f"Total files updated: {count}")

if __name__ == '__main__':
    fix()
