import os
import re

html_replacements = {
    '>Geri<': '>{{ _(\'Geri\') }}<',
    '>Anı Yakala,<': '>{{ _(\'Anı Yakala,\') }}<',
    '>Dünyayla Paylaş.<': '>{{ _(\'Dünyayla Paylaş.\') }}<',
    '>Sınırsız İlham<': '>{{ _(\'Sınırsız İlham\') }}<',
    '>Teknik Detaylar (EXIF)<': '>{{ _(\'Teknik Detaylar (EXIF)\') }}<',
    '>Profesyonel Topluluk<': '>{{ _(\'Profesyonel Topluluk\') }}<',
    '>Hakkımızda<': '>{{ _(\'Hakkımızda\') }}<',
    'KAMERAYI ÇALIŞTIR': '{{ _(\'KAMERAYI ÇALIŞTIR\') }}',
    '>Menü<': '>{{ _(\'Menü\') }}<',
    '>Profilim<': '>{{ _(\'Profilim\') }}<',
    '>Bildirimler<': '>{{ _(\'Bildirimler\') }}<',
    '>Ayarlar<': '>{{ _(\'Ayarlar\') }}<',
    '>Çıkış Yap<': '>{{ _(\'Çıkış Yap\') }}<',
    '>Giriş Yap<': '>{{ _(\'Giriş Yap\') }}<',
    '>Kayıt Ol<': '>{{ _(\'Kayıt Ol\') }}<',
    'FOTOĞRAF YÜKLE': '{{ _(\'FOTOĞRAF YÜKLE\') }}',
    '>Giriş<': '>{{ _(\'Giriş\') }}<',
    '>Kayıt<': '>{{ _(\'Kayıt\') }}<',
    '>Takip Edilenler<': '>{{ _(\'Takip Edilenler\') }}<',
    '>Keşfet<': '>{{ _(\'Keşfet\') }}<',
    '>Henüz fotoğraf yok<': '>{{ _(\'Henüz fotoğraf yok\') }}<',
    '>İlk Sen Yükle<': '>{{ _(\'İlk Sen Yükle\') }}<',
    'placeholder="Temalarda, kullanıcılarda veya fotoğraf başlıklarında ara..."': 'placeholder="{{ _(\'Temalarda, kullanıcılarda veya fotoğraf başlıklarında ara...\') }}"',
    'Profil & Hesap Yönetimi': '{{ _(\'Profil & Hesap Yönetimi\') }}',
}

base_dir = os.path.join(os.path.dirname(__file__), 'app', 'templates')
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            for k, v in html_replacements.items():
                if f"{{{{ _(" not in content or v not in content:
                    content = content.replace(k, v)
            
            # fix double wrapping
            content = content.replace('{{ _(\'{{ _(\'KAMERAYI ÇALIŞTIR\') }}\') }}', '{{ _(\'KAMERAYI ÇALIŞTIR\') }}')
            content = content.replace('{{ _(\'{{ _(\'FOTOĞRAF YÜKLE\') }}\') }}', '{{ _(\'FOTOĞRAF YÜKLE\') }}')
            
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(content)

print("HTML strings wrapped.")
