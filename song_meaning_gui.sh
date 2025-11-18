#!/usr/bin/env bash
set -e

echo "============================================"
echo "What Do Those Song Lyrics Mean? - Starting..."
echo "============================================"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed or not in PATH."
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi
echo "[OK] Python found"

# Check for pip
if ! python3 -m pip --version &> /dev/null; then
    echo "[INFO] Installing pip..."
    python3 -m ensurepip --upgrade || {
        echo "[ERROR] Could not install pip."
        exit 1
    }
fi
echo "[OK] pip found"

# Create virtual environment if missing
if [[ ! -d .venv ]]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv .venv || {
        echo "[ERROR] Unable to create virtual environment."
        exit 1
    }
    echo "[OK] Virtual environment created"
else
    echo "[OK] Virtual environment exists"
fi

# Activate virtual environment
echo "[INFO] Activating virtual environment..."
source .venv/bin/activate || {
    echo "[ERROR] Could not activate virtual environment."
    exit 1
}
echo "[OK] Virtual environment activated"

# Upgrade pip in venv
echo "[INFO] Upgrading pip..."
python -m pip install --quiet --upgrade pip

# Install dependencies
echo "[INFO] Installing dependencies (this may take a moment)..."
python -m pip install --quiet --disable-pip-version-check -r requirements.txt || {
    echo "[ERROR] Dependency installation failed."
    exit 1
}
echo "[OK] Dependencies installed"

# Install Playwright browsers
echo "[INFO] Installing Playwright browsers (one-time setup)..."
playwright install chromium || {
    echo "[WARNING] Playwright browser installation failed. Scraping may not work."
}
echo "[OK] Playwright browsers installed"

# Launch Streamlit and open browser
echo ""
echo "============================================"
echo "Starting Streamlit app..."
echo "Your browser should open to http://localhost:8501"
echo ""
echo "Get your FREE Groq API key at: https://console.groq.com"
echo ""
echo "Press Ctrl+C to stop the server."
echo "============================================"
echo ""

sleep 2

# Try to open browser (works on macOS and most Linux distros)
if command -v open &> /dev/null; then
    open http://localhost:8501 &
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8501 &
fi

streamlit run app.py

echo ""
echo "============================================"
echo "App stopped."
echo "============================================"
