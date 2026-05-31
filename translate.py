import os

filepath = r'C:\Users\ardap\.gemini\antigravity\scratch\ShutterGallery\app\translations\en\LC_MESSAGES\messages.po'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

translations = {
    'Kullanıcı Adı': 'Username',
    'E-posta': 'Email',
    'Biyografi': 'Bio',
    'Dil': 'Language',
    'Profil Fotoğrafı Güncelle': 'Update Profile Photo',
    'Güncelle': 'Update',
    'Bu kullanıcı adı alınmış. Lütfen başka bir tane seçin.': 'This username is taken. Please choose another one.',
    'Bu e-posta adresi zaten kullanımda.': 'This email address is already in use.',
    'Hesap bilgileriniz güncellendi!': 'Your account info has been updated!',
    '↔ Sürükle & Döndür &nbsp;·&nbsp; Scroll: Yakınlaş': '↔ Drag & Rotate &nbsp;·&nbsp; Scroll: Zoom in',
    'Anı Yakala,': 'Capture the Moment,',
    'Dünyayla Paylaş.': 'Share with the World.',
    'ShutterGallery, fotoğraf tutkunlarını bir araya getiren premium bir vitrindir. Sadece en iyi karelerin, en yüksek kalitede yer aldığı bağımsız fotoğrafçılık platformu.': 'ShutterGallery is a premium showcase bringing photography enthusiasts together. An independent photography platform where only the best shots take place in highest quality.',
    'Sınırsız İlham': 'Unlimited Inspiration',
    'Teknik Detaylar (EXIF)': 'Technical Details (EXIF)',
    'Profesyonel Topluluk': 'Professional Community',
    'Hakkımızda': 'About Us',
    '2026 yılında kurulan ShutterGallery, fotoğrafçıların yeteneklerini hiçbir algoritma baskısı olmadan sergileyebilmesi için özenle tasarlandı.': 'Established in 2026, ShutterGallery is carefully designed for photographers to showcase their talents without any algorithmic pressure.',
    'Kuruluş': 'Founded',
    'KAMERAYI ÇALIŞTIR': 'POWER ON CAMERA',
    'Menü': 'Menu',
    'Profilim': 'My Profile',
    'Bildirimler': 'Notifications',
    'Ayarlar': 'Settings',
    'Çıkış Yap': 'Logout',
    'Giriş Yap': 'Login',
    'Kayıt Ol': 'Register',
    'FOTOĞRAF YÜKLE': 'UPLOAD PHOTO',
    'Giriş': 'Login',
    'Kayıt': 'Register',
    'Takip Edilenler': 'Following',
    'Keşfet': 'Discover'
}

for i in range(len(lines)):
    if lines[i].startswith('msgid '):
        msgid = lines[i][7:-2]
        if msgid in translations:
            if i + 1 < len(lines) and lines[i+1].startswith('msgstr '):
                lines[i+1] = f'msgstr "{translations[msgid]}"\n'

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)
