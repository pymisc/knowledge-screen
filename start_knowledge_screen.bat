@echo off
REM ============================================================
REM Knowledge Screen - Windows Startup Launcher
REM ============================================================
REM
REM Purpose:
REM   Automatically launch Knowledge Screen after Windows login.
REM
REM The 60-second delay allows Windows, OneDrive, and connected
REM monitors to finish initializing before the application starts.
REM
REM %~dp0 represents the directory containing this BAT file,
REM so the script does not depend on a hard-coded project path.
REM ============================================================


REM ------------------------------------------------------------
REM Wait 60 seconds after Windows login
REM ------------------------------------------------------------
timeout /t 60 /nobreak >nul


REM ------------------------------------------------------------
REM Change to the Knowledge Screen project directory
REM ------------------------------------------------------------
cd /d "%~dp0"


REM ------------------------------------------------------------
REM Launch Knowledge Screen using the project's virtualenv
REM
REM Activating the virtual environment is NOT required because
REM we call its Python executable directly.
REM ------------------------------------------------------------
".venv\Scripts\python.exe" "knowledge_screen.py"


REM ------------------------------------------------------------
REM If the Python application exits, keep this window open so
REM any error or diagnostic message can be reviewed.
REM ------------------------------------------------------------
echo.
echo ============================================================
echo Knowledge Screen has stopped.
echo ============================================================
echo.
pause