# What Do Those Song Lyrics Mean? 🎵

A Streamlit app that finds song lyrics from YouTube and interprets them using **free AI** (Groq). No paywalls, no ads—just search by song name or paste a YouTube link.

Built following the **7D Agile** methodology: Discover, Define, Design, Develop, Debug, Deploy, Drive.

---

## ✨ Features

- 🔍 **Smart Search**: Enter "Artist - Song Name" or paste YouTube/YouTube Music URLs
- 🎬 **Auto Scraping**: Extracts captions/lyrics directly from YouTube videos
- 🤖 **Free AI**: Uses Groq's free LLM API (no OpenAI subscription needed)
- 🎨 **Clean UI**: Streamlit interface with expandable lyrics view
- 💾 **Privacy First**: API key stored in session only, never persisted

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Groq API Key** (free): Get one at [console.groq.com](https://console.groq.com)

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
2. Install all dependencies
3. Install Playwright browsers
4. Launch the Streamlit app
5. Open your browser automatically

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

1. **Get Your Free Groq API Key**:
   - Visit [console.groq.com](https://console.groq.com)
   - Sign up (free tier is generous)
   - Copy your API key (starts with `gsk_`)

2. **Launch the App**:
   - Run via script OR `streamlit run app.py`
   - App opens at `http://localhost:8501`

3. **Search for Lyrics**:
   - **Option A**: Type "Artist - Song Name" (e.g., `Radiohead - Karma Police`)
   - **Option B**: Paste a YouTube URL (e.g., `https://youtu.be/dQw4w9WgXcQ`)

4. **Get Interpretation**:
   - Click "🔍 Get Lyrics & Interpret"
   - View scraped lyrics and AI analysis

---

## 🏗️ Architecture (7D Agile)

| Phase | Implementation |
|-------|----------------|
| **DISCOVER** | Research free LLM APIs (Groq), YouTube scraping methods |
| **DEFINE** | Requirements: URL/song search, scraping, free AI, Streamlit UI |
| **DESIGN** | Modular structure: `scraper.py` + `app.py` + Groq integration |
| **DEVELOP** | Build scraper with Playwright, integrate Groq API, create UI |
| **DEBUG** | Error handling for missing captions, invalid URLs, API failures |
| **DEPLOY** | Setup scripts for Windows/Linux, clear documentation |
| **DRIVE** | Future: Add Spotify metadata, save interpretations, multi-lens analysis |

---

## 📁 Project Structure

```
what-do-those-song-lyrics-mean-gui/
├── app.py                    # Main Streamlit application
├── scraper.py                # YouTube scraping module
├── requirements.txt          # Python dependencies
├── .env.example             # API key template
├── song_meaning_gui.bat     # Windows launch script
├── song_meaning_gui.sh      # macOS/Linux launch script
├── README.md                # This file
└── Gillsystems_logo_with_donation_qrcodes.png
```

---

## 🔑 Environment Variables

Create a `.env` file (optional) to avoid entering API key each time:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Or use the sidebar input in the app (recommended for security).

---

## 🛠️ Technical Details

### Dependencies
- **streamlit**: Web UI framework
- **groq**: Free LLM API client (Llama 3.1)
- **playwright**: Browser automation for YouTube search
- **youtube-transcript-api**: Extract video captions
- **python-dotenv**: Environment variable management

### Scraping Logic
1. **URL Detection**: Parses YouTube/YouTube Music URLs
2. **Video ID Extraction**: Supports multiple URL formats
3. **Caption Retrieval**: Fetches manual or auto-generated transcripts
4. **Search Fallback**: If song name provided, searches YouTube first

### AI Model
- **Model**: `llama-3.1-70b-versatile` (Groq)
- **Free Tier**: 30 requests/min, 6000 tokens/min
- **Temperature**: 0.5 (balanced creativity/accuracy)
- **Max Tokens**: 600 (concise interpretations)

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
