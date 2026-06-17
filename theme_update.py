import os
import glob

replacements = {
    'bg-zinc-900': 'bg-[#FDFBF7]',
    'bg-zinc-800': 'bg-[#EAE6D9]',
    'text-white': 'text-[#2D3A2A]',
    'text-zinc-400': 'text-[#6B7A68]',
    'text-zinc-500': 'text-[#6B7A68]',
    'text-zinc-300': 'text-[#586B5A]',
    'text-zinc-200': 'text-[#586B5A]',
    'bg-emerald-600': 'bg-[#7B9A74]',
    'hover:bg-emerald-500': 'hover:bg-[#506B4D]',
    'text-emerald-400': 'text-[#7B9A74]',
    'text-emerald-500': 'text-[#506B4D]',
    'bg-emerald-500': 'bg-[#7B9A74]',
    'border-white/10': 'border-[#7B9A74]/20',
    'border-white/5': 'border-[#7B9A74]/10',
    'border-white/20': 'border-[#7B9A74]/30',
    'border-emerald-500/50': 'border-[#7B9A74]/50',
    'bg-black': 'bg-white',
    'bg-black/80': 'bg-white/80',
    'bg-black/40': 'bg-white/60',
    'bg-black/60': 'bg-white/70',
    'bg-black/50': 'bg-white/60',
    'text-red-500': 'text-[#D4A373]',
    'text-blue-400': 'text-[#7B9A74]',
    'bg-blue-600/20': 'bg-[#7B9A74]/20',
    'hover:bg-blue-600/40': 'hover:bg-[#7B9A74]/40',
    'border-blue-500/50': 'border-[#7B9A74]/50'
}

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

if __name__ == "__main__":
    templates_dir = "app/templates"
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith(".html"):
                update_file(os.path.join(root, file))
