import sys
import re

filepath = sys.argv[1]

# Rebase todo listesini düzenler
if 'git-rebase-todo' in filepath:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # İlk pick'i (yani baştan ikinci commit'i) reword yapar
    content = re.sub(r'^pick ', 'reword ', content, count=1, flags=re.MULTILINE)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Commit mesajını düzenler
elif 'COMMIT_EDITMSG' in filepath:
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("Frontend: Kullanici ozel ID'leri, sayfalama, 404/500 hata sayfalari ve dagitim ayarlari eklendi\n")
