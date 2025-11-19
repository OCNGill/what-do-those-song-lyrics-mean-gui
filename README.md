# What Do Those Song Lyrics Mean? 🎵

A Streamlit app that finds song lyrics from YouTube/YouTube Music and interprets them using **free AI** — works 100% locally (no API key needed) OR optionally with Groq cloud for faster/better results.

Built following the **7D Agile** methodology: Discover, Define, Design, Develop, Debug, Deploy, Drive.

---

## ✨ Features

- 🔍 **Smart Search**: Enter "Artist - Song Name" or paste YouTube/YouTube Music/Spotify URLs
- 🎬 **Auto Scraping**: 
  - YouTube videos with subtitles → Direct caption extraction
  - YouTube Music → Metadata extraction + AZLyrics search
  - Spotify → Track info + AZLyrics search
  - Manual search → AZLyrics lookup
- 🤖 **Two AI Modes**:
  - **Local CPU Mode** (default): Runs 100% locally, no API key needed (small model, slower, lower quality)
  - **Cloud Mode** (recommended): Use Groq's free API for **much better** interpretations
- 🖥️ **Hardware Detection**: Auto-detects CPU cores, RAM, and GPU availability
- 🎛️ **Model Selection**: Choose from 5 preset models or use custom HuggingFace model IDs
- 🎨 **Clean UI**: Streamlit interface with tabs for search/manual input
- 💾 **Privacy First**: Everything runs locally by default; optional cloud mode

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+**
- **Recommended**: Groq API Key for better AI quality (free at [console.groq.com](https://console.groq.com))

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

**⚠️ First Run Note**: Dependencies are ~2GB total (PyTorch + transformers). The local AI model (~308MB) downloads automatically on first use in local mode.

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

### Cloud Mode (Recommended for Best Quality) ⭐

**Why Cloud Mode?** The local CPU models produce poor quality output (slow, often nonsensical). Groq's cloud API is:
- ✅ **Free** (generous limits: 30 req/min, 6000 tokens/min)
- ✅ **Fast** (1-3 seconds vs 10-30 seconds)
- ✅ **High Quality** (uses llama-3.1-70b-versatile)
- ✅ **No GPU Needed**

1. **Get Your Free Groq API Key**:
   - Visit [console.groq.com](https://console.groq.com)
   - Sign up (free, no credit card required)
   - Create an API key (starts with `gsk_`)
   - Copy the key

2. **Launch the App**:
   - Run via script OR `streamlit run app.py`
   - App opens at `http://localhost:8501`

3. **Enter API Key** in the sidebar (or add to `.env` file)

4. **Keep "Use Local CPU Model" unchecked**

5. **Search for Lyrics**:
   - Type "Artist - Song Name" (e.g., `Pink Floyd - Time`)
   - OR paste a YouTube URL (e.g., `https://youtu.be/dQw4w9WgXcQ`)
   - OR paste a YouTube Music URL (e.g., `https://music.youtube.com/watch?v=...`)

6. **Get Interpretation**:
   - Click "🔍 Get Lyrics & Interpret"
   - View lyrics and high-quality AI interpretation

### Local Mode (No API Key - Lower Quality)

**⚠️ Note**: Local CPU models provide **poor quality** output and are **very slow** without a GPU. Only use this if you cannot access Groq's free cloud API.

1. **Launch the App**:
   - Run via script OR `streamlit run app.py`
   - App opens at `http://localhost:8501`

2. **Check "Use Local CPU Model"** in sidebar

3. **Select Model** (or use custom HuggingFace ID):
   - `flan-t5-small` (308MB) - Fastest but lowest quality
   - `flan-t5-base` (990MB) - Better quality, slower
   - `flan-t5-large` (2.9GB) - Best local quality, very slow on CPU

4. **Search for Lyrics** (same as cloud mode)

5. **Get Interpretation**:
   - Click "🔍 Get Lyrics & Interpret"
   - First run: downloads model (one-time, ~308MB-2.9GB depending on selection)
   - Expect 10-30 seconds processing time
   - Quality will be limited compared to cloud mode

---

## 🏗️ Architecture (7D Agile)

| Phase | Implementation |
|-------|----------------|
| **DISCOVER** | Research free LLM options (cloud + local), YouTube/AZLyrics scraping methods |
| **DEFINE** | Requirements: URL/song search, multi-source scraping, local AI fallback, optional cloud |
| **DESIGN** | Modular: `scraper_v2.py` + `hardware.py` + `app.py` with dual AI modes (local HF + Groq cloud) |
| **DEVELOP** | yt-dlp subtitle extraction, AZLyrics scraping, hardware detection, model selection UI |
| **DEBUG** | Fixed broken youtube-transcript-api, added fallback sources, improved error handling |
| **DEPLOY** | Setup scripts with PyTorch install, clear cloud vs local mode docs |
| **DRIVE** | Future: Genius API integration, GPU support, save interpretations, batch processing |

---

## 📁 Project Structure

```
what-do-those-song-lyrics-mean-gui/
├── app.py                    # Main Streamlit application v2.0
├── scraper_v2.py             # Multi-source lyrics scraper (YouTube/AZLyrics)
├── hardware.py               # Hardware detection & model recommendations
├── requirements.txt          # Python dependencies
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
# Recommended: Set Groq key for better quality
GROQ_API_KEY=your_groq_api_key_here

# Optional: Add Genius API token for additional lyrics sources
GENIUS_ACCESS_TOKEN=your_genius_token_here

# Optional: Add Spotify credentials for better track info extraction
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
```

If `GROQ_API_KEY` is not set, app defaults to local CPU mode (lower quality).

---

## 🛠️ Technical Details

### Lyrics Sources
1. **YouTube Subtitles** (yt-dlp) - Direct extraction from videos with captions
2. **AZLyrics** (web scraping) - Free lyrics database, no API key required
3. **Genius** (optional) - Requires free API token from [genius.com/api-clients](https://genius.com/api-clients)

### Dependencies
- **streamlit**: Web UI framework
- **groq**: Free cloud LLM API client (recommended)
- **yt-dlp**: YouTube subtitle extraction
- **beautifulsoup4 + lxml**: Web scraping for lyrics
- **transformers**: Hugging Face models for local inference
- **torch**: PyTorch CPU for local model execution
- **psutil**: Hardware detection (CPU/RAM/GPU)
- **python-dotenv**: Environment variable management

### AI Models

#### Cloud Mode (Recommended) ⭐
- **Model**: `llama-3.1-70b-versatile` (Groq)
- **Free Tier**: 30 requests/min, 6000 tokens/min
- **Speed**: ~1-3 seconds per interpretation
- **Quality**: Excellent, detailed analysis
- **Setup**: Free API key at [console.groq.com](https://console.groq.com)

#### Local Mode (Fallback)
- **Models**: 5 presets + custom HuggingFace IDs
  - `flan-t5-small` (~308MB) - Fast but low quality
  - `flan-t5-base` (~990MB) - Better quality, slower
  - `flan-t5-large` (~2.9GB) - Best local quality, very slow on CPU
  - `flan-t5-xl` (~11GB) - Requires GPU
  - `bart-large-cnn` (~1.6GB) - Alternative model
- **Device**: CPU only (GPU auto-detected if available)
- **First Run**: Downloads model automatically
- **Speed**: ~10-30 seconds per interpretation (CPU-dependent)
- **Quality**: Limited, often produces nonsensical output on CPU

**⚠️ Performance Note**: Without a GPU, local models provide poor quality results. Cloud mode (Groq) is **strongly recommended** for usable output.

---

## 🐛 Troubleshooting

### "No transcript/lyrics available"
- YouTube videos without subtitles → Try "Artist - Song Name" manual search
- AZLyrics requires exact artist/song names → Check spelling
- Try adding video to YouTube Music and using that URL

### AI Output is Nonsense (Local Mode)
- **Solution**: Use Groq cloud mode instead (free, much better quality)
- Local CPU models are not powerful enough for quality analysis
- If you must use local: Try `flan-t5-base` or `flan-t5-large` (slower but better)
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
- [x] Spotify metadata extraction
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
