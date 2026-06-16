import urllib.request
import urllib.error

routes = [
    '/',
    '/discover',
    '/search',
    '/auth/login',
    '/auth/register',
    '/users/profile/ardap00',
    '/users/gallery/ardap00'
]

for route in routes:
    url = f"https://shuttergallery.xyz{route}"
    try:
        response = urllib.request.urlopen(url)
        print(f"GET {route} -> {response.getcode()}")
    except urllib.error.HTTPError as e:
        print(f"GET {route} -> HTTP {e.code}")
    except Exception as e:
        print(f"GET {route} -> Error: {e}")
