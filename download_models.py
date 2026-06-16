import os
import urllib.request

MODELS_DIR = 'app/static/models'
os.makedirs(MODELS_DIR, exist_ok=True)

models = {
    'Nefertiti.glb': 'https://raw.githubusercontent.com/mrdoob/three.js/master/examples/models/gltf/Nefertiti/Nefertiti.glb',
    'SheenChair.glb': 'https://raw.githubusercontent.com/mrdoob/three.js/master/examples/models/gltf/SheenChair.glb'
}

for filename, url in models.items():
    filepath = os.path.join(MODELS_DIR, filename)
    print(f"Downloading {filename} from {url}...")
    try:
        urllib.request.urlretrieve(url, filepath)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}. Error: {e}")
