# Song Lyric Explainer · 7D Agile Edition

A Streamlit-powered companion that breaks down any set of lyrics with a musicologist's voice. It follows Professor Lysakowski's 7D Agile expectations: disciplined structure, tight logging, and expandable architecture (swap models, add telemetry, or bolt on repo utilities later).

## Prerequisites
- Python 3.10+
- An OpenAI API key with access to `gpt-4o-mini` (get one at https://platform.openai.com/api-keys)

## Quick Start

**Windows:** Double-click `song_meaning_gui.bat` (opens cmd window automatically)

**macOS/Linux:** Run `./song_meaning_gui.sh` (may need `chmod +x song_meaning_gui.sh` first)

The script will:
1. Create a virtual environment if needed
2. Install dependencies
3. Launch Streamlit
4. Open your browser to the app

**Enter your OpenAI API key in the sidebar when the app opens.**

## Manual Install & Run

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL (default: <http://localhost:8501>).

### Quick launch scripts
Prefer a one-command experience? Use the helper scripts in the repo root after setting your API key:

```powershell
song_meaning_gui.bat
```

```bash
./song_meaning_gui.sh
```

> If your shell reports a permission error, run `chmod +x song_meaning_gui.sh` once.

Each script checks for `OPENAI_API_KEY`, ensures `.venv` exists, installs dependencies, and then launches `streamlit run app.py` for you.

## Feature highlights
- **Dark UI** tuned for classroom screens with accent colors ready for your logo drop-in.
- **Modular OpenAI wrapper** so future model swaps (Azure, vLLM, Anthropic) are one function away.
- **Context-rich copy**: synopsis, two thematic insights, and a discussion question under 200 words.
- **Guardrails**: friendly warnings for missing lyrics or API keys, structured logging, and cached client init.

## 7D Agile mapping
| Phase | Implementation detail |
| --- | --- |
| DEFINE | Sidebar instructions and inline guidance clarify the user's intent before execution. |
| DESIGN | Prompt template and dark-theme config live alongside requirements for easy revision. |
| DEVELOP | `app.py` keeps business logic under ~100 lines, separating prompt craft, client init, and UI. |
| DEBUG | Logging + surfaced error captions make it simple to trace failures (bad key, network, etc.). |
| DOCUMENT | This README plus inline docstrings outline usage, configuration, and rationale. |
| DELIVER | Streamlit packaging (requirements + config) enables fast classroom demos. |
| DEPLOY | `.gitignore`, theme config, and env-based auth keep the repo production-friendly. |

Contributions and forks are welcome—just keep the 7D discipline intact.

<p align="center">
	<img src="Gillsystems_logo_with_donation_qrcodes.png" alt="Gillsystems logo" width="360" />
</p>
