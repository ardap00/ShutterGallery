import os
import re

def fix_theme():
    templates_dir = os.path.join(os.path.dirname(__file__), 'app', 'templates')
    
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                original = content
                
                # Replace any previous attempts
                content = content.replace('[#9CA986]', '[#A3B18A]')
                content = content.replace('[#8B9876]', '[#588157]')
                content = content.replace('[#D5C4A1]', '[#DAD7CD]')
                
                # Bruteforce ANY emerald references
                content = re.sub(r'emerald-[1-9]00', '[#A3B18A]', content)
                content = re.sub(r'text-emerald-500', 'text-[#A3B18A]', content)
                content = re.sub(r'bg-emerald-600', 'bg-[#829A73]', content)
                content = re.sub(r'bg-emerald-500', 'bg-[#A3B18A]', content)
                content = re.sub(r'border-emerald-500', 'border-[#A3B18A]', content)
                content = re.sub(r'text-emerald-400', 'text-[#A3B18A]', content)
                
                # Handle shadows that contain emerald rgba
                content = re.sub(r'16,\s*185,\s*129', '163,177,138', content)
                
                # Change the background image to the proper gallery
                content = re.sub(
                    r"url\('https://images\.unsplash\.com/photo-1536924940846-227afb31e2a5.*?'\)",
                    "url('https://images.unsplash.com/photo-1577720580479-7d839d829c73?q=80&w=1920')",
                    content
                )
                content = re.sub(
                    r"url\('https://images\.unsplash\.com/photo-1506905925346-21bda4d32df4.*?'\)",
                    "url('https://images.unsplash.com/photo-1577720580479-7d839d829c73?q=80&w=1920')",
                    content
                )

                content = content.replace('filter: blur(28px) brightness(30%);', 'filter: blur(4px) brightness(20%);')
                
                if content != original:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated {filepath}")

if __name__ == '__main__':
    fix_theme()
