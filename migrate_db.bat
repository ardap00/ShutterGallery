@echo off
set FLASK_APP=run.py
venv\Scripts\flask.exe db migrate -m "Add language to User"
venv\Scripts\flask.exe db upgrade
pause
