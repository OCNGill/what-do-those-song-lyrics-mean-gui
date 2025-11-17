#!/usr/bin/env bash
set -euo pipefail

if [[ -z "${OPENAI_API_KEY:-}" ]]; then
  echo "[ERROR] Please export OPENAI_API_KEY before running this script." >&2
  echo "Example: export OPENAI_API_KEY=sk-your-key" >&2
  exit 1
fi

if [[ ! -d .venv ]]; then
  echo "[INFO] Creating virtual environment (.venv)..."
  python3 -m venv .venv
fi

source .venv/bin/activate

echo "[INFO] Installing dependencies..."
pip install --disable-pip-version-check -r requirements.txt

echo "[INFO] Launching Streamlit..."
streamlit run app.py
