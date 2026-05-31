@echo off
"C:\Program Files\Git\cmd\git.exe" rebase --abort
"C:\Program Files\Git\cmd\git.exe" fetch
"C:\Program Files\Git\cmd\git.exe" reset --hard origin/main
pause
