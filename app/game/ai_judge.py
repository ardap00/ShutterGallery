import os
import json
import base64
import urllib.request
import urllib.error
from flask import current_app

THEMES = [
    {"theme": "Altın Saat (Golden Hour)", "desc": "Gün batımı veya gün doğumundaki sıcak, yumuşak ışık ve uzun gölgeler."},
    {"theme": "Minimalizm & Boşluk", "desc": "Sade kompozisyon, tek bir odak noktası ve geniş negatif alan."},
    {"theme": "Geometrik Çizgiler", "desc": "Mimaride veya doğada tekrar eden çizgiler, simetri ve perspektif."},
    {"theme": "Duygu Dolu Portre", "desc": "Bir insanın veya canlının bakışlarındaki samimi duygu ve derinlik."},
    {"theme": "Sokak Hayatı (Street Life)", "desc": "Gündelik hayatın telaşından yakalanmış habersiz, dinamik bir an."},
    {"theme": "Doğanın Dokusu (Macro/Texture)", "desc": "Yaprak damarları, taş dokusu, su damlacıkları gibi mikro detaylar."},
    {"theme": "Gece & Işık Oyunları", "desc": "Karanlıkta parlayan neonlar, araç ışık izleri veya ay ışığı."},
    {"theme": "Siyah & Beyaz Kontrast", "desc": "Işık ve gölgenin saf dramatik dansı, yüksek kontrast."},
    {"theme": "Yansımalar & Aynalar", "desc": "Su birikintisi, cam veya aynada oluşan büyüleyici yansımalar."},
    {"theme": "Hareket & Dinamizm", "desc": "Akan su, koşan bir canlı veya hareket hissi veren estetik bulanıklık."},
    {"theme": "Retro & Nostalji", "desc": "Eski zamanları hatırlatan sıcak tonlar, nostaljik objeler veya mekanlar."},
    {"theme": "Yalnızlık & Sessizlik", "desc": "Tek başına bir figür, boş bir bank veya terk edilmiş sakin bir köşe."}
]

def get_random_theme(used_themes=None):
    import random
    if not used_themes:
        return random.choice(THEMES)
    available = [t for t in THEMES if t["theme"] not in used_themes]
    if not available:
        available = THEMES
    return random.choice(available)

def _image_to_base64_and_mime(image_ref):
    """
    Takes an image reference (Cloudinary URL or local filename in uploads)
    and returns (base64_data, mime_type).
    """
    if image_ref.startswith('http://') or image_ref.startswith('https://'):
        req = urllib.request.Request(image_ref, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            content_type = resp.headers.get('Content-Type', 'image/jpeg').split(';')[0]
            return base64.b64encode(data).decode('utf-8'), content_type
    else:
        local_path = os.path.join(current_app.root_path, 'static', 'uploads', image_ref)
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Görsel dosyası bulunamadı: {image_ref}")
        
        ext = os.path.splitext(local_path)[1].lower()
        mime_type = 'image/png' if ext == '.png' else ('image/webp' if ext == '.webp' else 'image/jpeg')
        with open(local_path, 'rb') as f:
            data = f.read()
            return base64.b64encode(data).decode('utf-8'), mime_type

def judge_round(theme_name, theme_desc, p1_username, p1_img, p2_username, p2_img):
    """
    Evaluates two photos using Gemini 2.0 / 1.5 Flash via REST API.
    Returns:
    {
        "winner": "player1" | "player2" | "tie",
        "reasoning": "...",
        "feedback_p1": "...",
        "feedback_p2": "..."
    }
    """
    api_key = current_app.config.get('GEMINI_API_KEY') or os.environ.get('GEMINI_API_KEY') or os.environ.get('Gemini_API_Key') or os.environ.get('GOOGLE_API_KEY')
    model_name = current_app.config.get('GEMINI_MODEL') or 'gemini-3.5-flash'
    
    if not api_key:
        return {
            "winner": "tie",
            "reasoning": "Gemini API Key tanımlanmadığı için değerlendirme yapılamadı, tur berabere sayıldı.",
            "feedback_p1": "API anahtarı eksik.",
            "feedback_p2": "API anahtarı eksik."
        }

    try:
        p1_b64, p1_mime = _image_to_base64_and_mime(p1_img)
        p2_b64, p2_mime = _image_to_base64_and_mime(p2_img)
    except Exception as e:
        return {
            "winner": "tie",
            "reasoning": f"Görseller okunurken hata oluştu: {str(e)}",
            "feedback_p1": "",
            "feedback_p2": ""
        }

    prompt = f"""Sen profesyonel, saygın ve adil bir fotoğraf yarışması jürisisin.
İki fotoğrafçı birbiriyle yarışıyor.
Mevcut Turun Teması: "{theme_name}"
Tema Açıklaması: "{theme_desc}"

Fotoğraf 1 ({p1_username} tarafından çekildi)
Fotoğraf 2 ({p2_username} tarafından çekildi)

Lütfen iki fotoğrafı şu kriterlere göre detaylıca incele:
1. Temaya Uygunluk: Fotoğraf verilen temayı ve atmosferi ne kadar iyi yansıtıyor?
2. Kompozisyon & Kadraj: Üçler kuralı, yönlendirici çizgiler, denge, odak noktası.
3. Işık & Renk / Kontrast: Işık kullanımı, pozlama doğruluğu, renk uyumu veya gölge tonları.
4. Hikaye & Duygu: İzleyicide uyandırdığı görsel etki.

Lütfen kesinlikle aşağıdaki JSON şablonunda cevap ver. JSON dışında hiçbir metin, markdown veya açıklama yazma:
{{
  "winner": "player1" veya "player2" veya "tie",
  "reasoning": "Neden bu fotoğrafın kazandığına dair 2-3 cümlelik adil jüri kararı.",
  "feedback_p1": "{p1_username} için fotoğrafının güçlü yönleri ve 1 tavsiye (1-2 cümle).",
  "feedback_p2": "{p2_username} için fotoğrafının güçlü yönleri ve 1 tavsiye (1-2 cümle)."
}}
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": p1_mime,
                            "data": p1_b64
                        }
                    },
                    {
                        "inline_data": {
                            "mime_type": p2_mime,
                            "data": p2_b64
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "response_mime_type": "application/json"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=40) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            candidates = res_data.get('candidates', [])
            if candidates:
                text_part = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
                clean_text = text_part.strip()
                if clean_text.startswith('```json'):
                    clean_text = clean_text[7:]
                if clean_text.endswith('```'):
                    clean_text = clean_text[:-3]
                clean_text = clean_text.strip()
                
                result_json = json.loads(clean_text)
                return {
                    "winner": result_json.get("winner", "tie"),
                    "reasoning": result_json.get("reasoning", "Jüri kararı tamamlandı."),
                    "feedback_p1": result_json.get("feedback_p1", ""),
                    "feedback_p2": result_json.get("feedback_p2", "")
                }
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return {
            "winner": "tie",
            "reasoning": f"Yapay zeka analizi sırasında bir bağlantı hatası oluştu ({str(e)}). Tur berabere sayıldı.",
            "feedback_p1": "",
            "feedback_p2": ""
        }

    return {
        "winner": "tie",
        "reasoning": "Analiz tamamlanamadı.",
        "feedback_p1": "",
        "feedback_p2": ""
    }

