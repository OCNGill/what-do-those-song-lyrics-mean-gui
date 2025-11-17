@echo off
setlocal EnableDelayedExpansion

if not exist .venv (
    echo [INFO] Creating virtual environment (.venv)...
    python -m venv .venv || (
        echo [ERROR] Unable to create virtual environment.
        pause
        exit /b 1
    )
)

call .\.venv\Scripts\activate

echo [INFO] Installing dependencies...
pip install --disable-pip-version-check -r requirements.txt || (
    echo [ERROR] Dependency installation failed.
    pause
    exit /b 1
)

echo [INFO] Launching Streamlit...
echo Enter your OpenAI API key in the sidebar when the app opens.
echo.
streamlit run app.py
if errorlevel 1 (
    echo.
    echo [ERROR] Streamlit failed to start.
    pause
)
