# YouTube Scraper Fix - v2.0

## Problem
The `youtube-transcript-api` library was completely broken, returning XML parse errors for all videos.

## Solution
Created `scraper_v2.py` using `yt-dlp` as a replacement with these improvements:

### Key Changes:
1. **Replaced youtube-transcript-api with yt-dlp** - More reliable and actively maintained
2. **Fixed XML parsing** - YouTube subtitles use `<p>` tags, not `<text>` tags
3. **Preferred subtitle formats** - Priority: srv3 > vtt > srv2 > srv1 > json3
4. **Multi-source fallback** - YouTube → Genius.com (optional) → manual input
5. **Support for YouTube Music** - Same video ID extraction works for both

### What Works Now:
- ✅ YouTube videos with subtitles (manual or auto-generated)
- ✅ YouTube Music URLs (extracts video ID and gets subtitles)
- ✅ Clean, human-readable lyrics output
- ✅ Genius.com fallback (optional - requires GENIUS_ACCESS_TOKEN in .env)
- ✅ Graceful fallback to manual input if all sources fail

### What Doesn't Work Yet:
- ❌ Videos without subtitles (no alternative source)
- ⚠️ Genius.com requires API token (free but needs signup)
- ⚠️ Spotify only provides metadata, not lyrics (by API design)

### Testing Results:
```
Rick Astley - Never Gonna Give You Up: ✅ 2089 characters extracted
Zach Williams - Stand Up: ❌ No subtitles available
```

### Integration:
Updated `app.py` to import from `scraper_v2` instead of `scraper`. The app now successfully scrapes lyrics from YouTube videos with subtitles.

### Files Changed:
- `app.py` - Changed import from `scraper` to `scraper_v2`
- `scraper_v2.py` - New scraper implementation
- `requirements.txt` - Added yt-dlp, lyricsgenius, spotipy, beautifulsoup4, lxml

### Next Steps:
- Optional: Set up Genius API token for broader lyrics coverage
- Optional: Add user-facing error messages explaining why certain videos don't work
