@echo off
setlocal
cd /d "%~dp0"

echo ==============================================
echo Construction Daily Report Test
echo ==============================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set "PY=py"
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set "PY=python"
    ) else (
        echo Python was not found.
        echo Install Python first, then run this file again.
        pause
        exit /b 1
    )
)

echo Installing Flask...
%PY% -m pip install flask
if errorlevel 1 (
    echo.
    echo Flask installation failed.
    pause
    exit /b 1
)

echo.
echo Starting server...
echo If Windows Firewall asks, allow access on Private networks.
echo.
%PY% app.py

echo.
pause
