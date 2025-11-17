@echo off
setlocal EnableDelayedExpansion

@echo off
echo ============================================
echo Song Lyric Explainer - Starting...
echo ============================================
echo.

REM Ensure Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)
echo [OK] Python found

echo [OK] Python found

REM Ensure pip is installed
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing pip...
    python -m ensurepip --upgrade
    if errorlevel 1 (
        echo [ERROR] Could not install pip.
        pause
        exit /b 1
    )
)
echo [OK] pip found

echo [OK] pip found

REM Create virtual environment if missing
if not exist .venv (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Unable to create virtual environment.
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call .\.venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Could not activate virtual environment.
    pause
    exit /b 1
)
echo [OK] Virtual environment activated

REM Upgrade pip in venv
echo [INFO] Upgrading pip...
python -m pip install --quiet --upgrade pip

REM Install dependencies
echo [INFO] Installing dependencies (this may take a moment)...
python -m pip install --quiet --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Dependency installation failed.
    pause
    exit /b 1
)
echo [OK] Dependencies installed

echo [OK] Dependencies installed

REM Launch Streamlit and open browser
echo.
echo ============================================
echo Starting Streamlit app...
echo Your browser will open to http://localhost:8501
echo.
echo Enter your OpenAI API key in the sidebar.
echo.
echo Press Ctrl+C to stop the server.
echo ============================================
echo.

timeout /t 2 /nobreak >nul
start "" http://localhost:8501

streamlit run app.py

echo.
echo ============================================
echo App stopped.
echo ============================================
pause
