import os
import glob
count = 0
for filepath in glob.glob('app/templates/**/*.html', recursive=True):
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if '{{ _(' in line:
                print(f"{filepath}: {line.strip()}")
                count += 1
print(f"Total found: {count}")
