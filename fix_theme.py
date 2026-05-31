import os
import glob

def fix_theme():
    templates_dir = os.path.join('app', 'templates')
    files = glob.glob(f'{templates_dir}/**/*.html', recursive=True)
    
    for filepath in files:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original = content
        
        # Change the pastel green to an even softer sage green, and coffee to a lighter beige
        content = content.replace('[#9CA986]', '[#A3B18A]')
        content = content.replace('[#8B9876]', '[#588157]')
        content = content.replace('[#D5C4A1]', '[#DAD7CD]')
        content = content.replace('156,169,134', '163,177,138') # rgba for shadows
        
        # Catch ANY leftover emerald classes!
        import re
        content = re.sub(r'emerald-[1-9]00', '[#A3B18A]', content)
        content = re.sub(r'16,\s*185,\s*129', '163,177,138', content)
        
        # Change background image to a real art gallery with paintings
        content = content.replace(
            "url('https://images.unsplash.com/photo-1536924940846-227afb31e2a5?q=80&w=1920')",
            "url('https://images.unsplash.com/photo-1577720580479-7d839d829c73?q=80&w=1920')"
        )
        # Also catch the older background just in case
        content = content.replace(
            "url('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80')",
            "url('https://images.unsplash.com/photo-1577720580479-7d839d829c73?q=80&w=1920')"
        )
        content = content.replace(
            "url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?w=1920&q=80')",
            "url('https://images.unsplash.com/photo-1577720580479-7d839d829c73?q=80&w=1920')"
        )

        # Make sure brightness is correctly applied to act as a black transparent curtain
        content = content.replace('filter: brightness(25%) blur(2px);', 'filter: brightness(20%) blur(4px);')
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated {filepath}")

if __name__ == '__main__':
    fix_theme()
