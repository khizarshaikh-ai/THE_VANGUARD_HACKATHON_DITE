@echo off
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe (
  py -3 -m venv .venv
  if errorlevel 1 goto fail
)
.venv\Scripts\python.exe -c "import flask, sklearn, waitress" 2>nul
if errorlevel 1 (
  .venv\Scripts\python.exe -m pip install -r requirements.txt
  if errorlevel 1 goto fail
)
.venv\Scripts\python.exe launch.py
goto end
:fail
echo Setup failed. Install Python 3.13 or 3.14 and check the error above.
:end
pause
