# What Do Those Song Lyrics Mean? 🎵

A Streamlit app that finds song lyrics from YouTube and interprets them using **free AI** — works 100% locally (no API key needed) OR optionally with Groq cloud for faster/better results.

Built following the **7D Agile** methodology: Discover, Define, Design, Develop, Debug, Deploy, Drive.

---

## ✨ Features

- 🔍 **Smart Search**: Enter "Artist - Song Name" or paste YouTube/YouTube Music URLs
- 🎬 **Auto Scraping**: Extracts captions/lyrics directly from YouTube videos
- 🤖 **Two AI Modes**:
  - **Local CPU Mode** (default): Runs 100% locally, no API key needed (~80MB model download on first run)
  - **Cloud Mode** (optional): Use Groq's free API for faster/better interpretations
- 🎨 **Clean UI**: Streamlit interface with expandable lyrics view
- 💾 **Privacy First**: Everything runs locally by default; optional cloud mode

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Optional**: Groq API Key for cloud mode (free at [console.groq.com](https://console.groq.com))

### Installation

**Windows:**
```powershell
# Clone or download this repo
cd what-do-those-song-lyrics-mean-gui

# Run the setup script
.\song_meaning_gui.bat
```

**macOS/Linux:**
```bash
# Clone or download this repo
cd what-do-those-song-lyrics-mean-gui

# Make script executable
chmod +x song_meaning_gui.sh

# Run the setup script
./song_meaning_gui.sh
```

The script will:
1. Create a Python virtual environment
2. Install all dependencies (including PyTorch CPU + transformers)
3. Install Playwright browsers
4. Launch the Streamlit app
5. Open your browser automatically

**⚠️ First Run Note**: Dependencies are ~2GB total (PyTorch + transformers). The local AI model (~80MB) downloads automatically on first use in local mode.

---

## 🔧 Manual Setup

If you prefer manual installation:

```powershell
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run the app
streamlit run app.py
```

---

## 📖 Usage

### Local Mode (No API Key Needed - Default)

1. **Launch the App**:
   - Run via script OR `streamlit run app.py`
   - App opens at `http://localhost:8501`

2. **Check "Use Local CPU Model"** in sidebar (enabled by default)

3. **Search for Lyrics**:
   - Type "Artist - Song Name" (e.g., `Radiohead - Karma Police`)
   - OR paste a YouTube URL (e.g., `https://youtu.be/dQw4w9WgXcQ`)

4. **Get Interpretation**:
   - Click "🔍 Get Lyrics & Interpret"
   - First run: downloads ~80MB model (one-time)
   - View lyrics and AI interpretation

### Cloud Mode (Optional - Better Quality)

1. **Get Your Free Groq API Key**:
   - Visit [console.groq.com](https://console.groq.com)
   - Sign up (free tier is generous)
   - Copy your API key (starts with `gsk_`)

2. **Uncheck "Use Local CPU Model"** in sidebar

3. **Enter API key** in the sidebar input

4. **Search and interpret** as above (faster, better quality)

---

## 🏗️ Architecture (7D Agile)

| Phase | Implementation |
|-------|----------------|
| **DISCOVER** | Research free LLM options (cloud + local), YouTube scraping methods |
| **DEFINE** | Requirements: URL/song search, scraping, local AI fallback, no mandatory keys |
| **DESIGN** | Modular: `scraper.py` + `app.py` with dual AI modes (local HF + Groq cloud) |
| **DEVELOP** | Playwright scraper, local CPU model (flan-t5-small), Groq cloud option, Streamlit UI |
| **DEBUG** | Error handling for missing captions, model loading, API failures |
| **DEPLOY** | Setup scripts with PyTorch install, clear local vs cloud mode docs |
| **DRIVE** | Future: GPU support, save interpretations, multi-lens analysis, batch processing |

---

## 📁 Project Structure

```
what-do-those-song-lyrics-mean-gui/
├── app.py                    # Main Streamlit application with dual AI modes
├── scraper.py                # YouTube scraping module
├── requirements.txt          # Python dependencies (includes PyTorch CPU + transformers)
├── .env.example             # Optional API key template
├── song_meaning_gui.bat     # Windows launch script
├── song_meaning_gui.sh      # macOS/Linux launch script
├── README.md                # This file
└── Gillsystems_logo_with_donation_qrcodes.png
```

---

## 🔑 Environment Variables (Optional)

Create a `.env` file to set default mode:

```env
# Optional: Set Groq key to default to cloud mode
GROQ_API_KEY=your_groq_api_key_here
```

If not set, app defaults to local CPU mode (no key needed).

---

## 🛠️ Technical Details

### Dependencies
- **streamlit**: Web UI framework
- **groq** (optional): Free cloud LLM API client
- **playwright**: Browser automation for YouTube search
- **youtube-transcript-api**: Extract video captions
- **transformers**: Hugging Face models for local inference
- **torch**: PyTorch CPU for local model execution
- **python-dotenv**: Environment variable management

### AI Models

#### Local Mode (Default)
- **Model**: `google/flan-t5-small` (~80MB)
- **Device**: CPU only (no GPU required)
- **First Run**: Downloads model automatically
- **Speed**: ~5-15 seconds per interpretation (CPU-dependent)
- **Quality**: Good for basic analysis

#### Cloud Mode (Optional)
- **Model**: `llama-3.1-70b-versatile` (Groq)
- **Free Tier**: 30 requests/min, 6000 tokens/min
- **Speed**: ~1-3 seconds per interpretation
- **Quality**: Excellent, detailed analysis

---

## 🐛 Troubleshooting

### "No transcript available"
- Not all YouTube videos have captions
- Try searching with "Artist - Song Name" to find lyric videos
- Look for official music videos or lyric videos

### "Could not find video"
- Playwright search may time out
- Try pasting the YouTube URL directly
- Check your internet connection

### "Groq API error"
- Verify your API key is correct
- Check free tier limits at [console.groq.com](https://console.groq.com)
- Wait a moment if rate-limited

### Playwright browser not installed
```bash
playwright install chromium
```

---

## 🔮 Future Enhancements

- [ ] Save interpretations to JSON with metadata
- [ ] Multiple interpretation "lenses" (personal, critical, spiritual)
- [ ] Spotify metadata extraction
- [ ] Batch processing for playlists
- [ ] Export to PDF/Markdown

---

## 🤝 Contributing

Contributions welcome! Follow the 7D Agile methodology:
1. **Discover**: Research the feature/fix
2. **Define**: Clear requirements
3. **Design**: Architecture plan
4. **Develop**: Write clean, documented code
5. **Debug**: Test thoroughly
6. **Deploy**: Update docs and scripts
7. **Drive**: Monitor and iterate

---

## 📄 License

Open source - feel free to use, modify, and share.

---

<p align="center">
  <img src="Gillsystems_logo_with_donation_qrcodes.png" alt="Gillsystems Logo" width="400" />
</p>

<p align="center">
  <strong>Built with ❤️ following 7D Agile principles</strong>
</p>
