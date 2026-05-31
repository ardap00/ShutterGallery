@echo off
cd C:\Users\ardap\.gemini\antigravity\scratch\ShutterGallery
set FLASK_APP=run.py
set FLASK_DEBUG=1
venv\Scripts\flask run --port 5000
