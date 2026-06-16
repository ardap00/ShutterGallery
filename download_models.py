import os
import urllib.request

MODELS_DIR = 'app/static/models'
os.makedirs(MODELS_DIR, exist_ok=True)

url = "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Assets/main/Models/AntiqueCamera/glTF-Binary/AntiqueCamera.glb"
filename = "AntiqueCamera.glb"
filepath = os.path.join(MODELS_DIR, filename)

print(f"Downloading {filename} from {url}...")
try:
    urllib.request.urlretrieve(url, filepath)
    print(f"Successfully downloaded {filename}")
except Exception as e:
    print(f"Failed to download {filename}. Error: {e}")
