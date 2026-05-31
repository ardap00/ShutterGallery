@echo off
"C:\Program Files\Git\cmd\git.exe" stash
set GIT_SEQUENCE_EDITOR="%CD%\venv\Scripts\python.exe" "%CD%\rebase_script.py"
set GIT_EDITOR="%CD%\venv\Scripts\python.exe" "%CD%\rebase_script.py"
"C:\Program Files\Git\cmd\git.exe" rebase -i HEAD~3
"C:\Program Files\Git\cmd\git.exe" push --force
"C:\Program Files\Git\cmd\git.exe" stash pop
pause
