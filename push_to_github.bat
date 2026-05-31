@echo off
"C:\Program Files\Git\cmd\git.exe" init
"C:\Program Files\Git\cmd\git.exe" add .
"C:\Program Files\Git\cmd\git.exe" commit -m "Frontend: Add user unique IDs, pagination, 404/500 error pages and deployment configs"
"C:\Program Files\Git\cmd\git.exe" branch -M main
"C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/ardap00/ShutterGallery.git
"C:\Program Files\Git\cmd\git.exe" push -u origin main
pause
