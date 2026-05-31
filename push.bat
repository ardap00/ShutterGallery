@echo off
set GIT_EXE=C:\Users\ardap\AppData\Local\Programs\Git\cmd\git.exe
%GIT_EXE% add .
%GIT_EXE% commit -m "Update application theme to Art Gallery style (Pastel green and milky coffee colors, gallery wall backgrounds)"
%GIT_EXE% push origin main
