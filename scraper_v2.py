"""
Enhanced scraper module for extracting lyrics from YouTube, YouTube Music, and Spotify.
Uses multiple methods: yt-dlp for subtitles, Genius API for lyrics, Spotify API for metadata.
"""
from __future__ import annotations

import logging
import re
from typing import Optional, Tuple
from urllib.parse import parse_qs, urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from various URL formats.
    
    Supports:
    - youtube.com/watch?v=VIDEO_ID
    - youtu.be/VIDEO_ID
    - youtube.com/embed/VIDEO_ID
    - music.youtube.com/watch?v=VIDEO_ID
    """
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'music\.youtube\.com\/watch\?v=([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # Try parsing query parameters
    try:
        parsed = urlparse(url)
        if 'youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc or 'music.youtube' in parsed.netloc:
            query_params = parse_qs(parsed.query)
            if 'v' in query_params:
                return query_params['v'][0]
    except Exception as e:
        logger.error(f"Error parsing URL: {e}")
    
    return None


def extract_spotify_track_id(url: str) -> Optional[str]:
    """Extract Spotify track ID from URL."""
    patterns = [
        r'spotify\.com/track/([a-zA-Z0-9]+)',
        r'spotify:track:([a-zA-Z0-9]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def is_youtube_url(text: str) -> bool:
    """Check if the input text is a YouTube or YouTube Music URL."""
    youtube_domains = ['youtube.com', 'youtu.be', 'music.youtube.com']
    return any(domain in text.lower() for domain in youtube_domains)


def is_youtube_music_url(text: str) -> bool:
    """Check if the input text is specifically a YouTube Music URL."""
    return 'music.youtube.com' in text.lower()


def is_spotify_url(text: str) -> bool:
    """Check if the input text is a Spotify URL."""
    return 'spotify.com' in text.lower() or 'spotify:' in text.lower()


def get_youtube_music_lyrics(url: str) -> Optional[str]:
    """
    Extract song info from YouTube Music URL and search for lyrics.
    YouTube Music requires authentication, so we extract metadata and search elsewhere.
    
    Args:
        url: Full YouTube Music URL
        
    Returns:
        Lyrics text or None
    """
    try:
        # Extract video ID and get metadata
        video_id = extract_video_id(url)
        if not video_id:
            return None
        
        title, artist = get_youtube_metadata(video_id)
        if title:
            logger.info(f"YouTube Music: {artist} - {title}, searching lyrics...")
            # Try Genius first
            lyrics = search_genius_lyrics(title, artist or "")
            if lyrics:
                return lyrics
            
            # Try lyrics-extractor as fallback
            lyrics = search_lyrics_extractor(title, artist or "")
            if lyrics:
                return lyrics
        
        return None
        
    except Exception as e:
        logger.error(f"Error processing YouTube Music URL: {e}")
        return None


def get_youtube_subtitles_ytdlp(video_id: str) -> Optional[str]:
    """
    Get subtitles using yt-dlp (more reliable than youtube-transcript-api).
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Subtitle text or None
    """
    try:
        import yt_dlp
        
        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en'],
            'quiet': True,
            'no_warnings': True,
        }
        
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Helper function to find preferred subtitle format
            def get_preferred_subtitle_url(subs):
                # Prefer srv3 (simple XML) or vtt formats over json3
                for fmt in ['srv3', 'vtt', 'srv2', 'srv1']:
                    for sub in subs:
                        if sub.get('ext') == fmt:
                            return sub.get('url')
                # Fallback to first available
                return subs[0]['url'] if subs else None
            
            # Try to get subtitles
            if 'subtitles' in info and 'en' in info['subtitles']:
                # Manual subtitles available
                sub_url = get_preferred_subtitle_url(info['subtitles']['en'])
                if sub_url:
                    logger.info(f"Found manual subtitles for {video_id}")
                    return _download_subtitle(sub_url)
            
            elif 'automatic_captions' in info and 'en' in info['automatic_captions']:
                # Auto-generated captions
                sub_url = get_preferred_subtitle_url(info['automatic_captions']['en'])
                if sub_url:
                    logger.info(f"Found auto-generated captions for {video_id}")
                    return _download_subtitle(sub_url)
            
            logger.warning(f"No subtitles found for {video_id}")
            return None
            
    except Exception as e:
        logger.error(f"yt-dlp error for {video_id}: {e}")
        return None


def _download_subtitle(url: str) -> Optional[str]:
    """Download and parse subtitle file."""
    try:
        import requests
        from bs4 import BeautifulSoup
        import warnings
        from bs4 import XMLParsedAsHTMLWarning
        
        # Suppress BeautifulSoup XML warning
        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse XML subtitles - YouTube uses <p> tags for text content
        soup = BeautifulSoup(response.content, 'lxml')
        texts = [p.get_text().strip() for p in soup.find_all('p')]
        
        if texts:
            # Join with newlines to preserve line structure
            full_text = '\n'.join(texts)
            # Clean up excessive whitespace within lines only
            lines = [re.sub(r'\s+', ' ', line).strip() for line in full_text.split('\n')]
            # Remove empty lines
            lines = [line for line in lines if line]
            return '\n'.join(lines)
        
        return None
    except Exception as e:
        logger.error(f"Error downloading subtitle: {e}")
        return None


def get_youtube_metadata(video_id: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Get video title and channel from YouTube.
    
    Returns:
        Tuple of (title, artist/channel)
    """
    try:
        import yt_dlp
        
        ydl_opts = {
            'skip_download': True,
            'quiet': True,
            'no_warnings': True,
        }
        
        url = f"https://www.youtube.com/watch?v={video_id}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', '')
            artist = info.get('uploader', '') or info.get('channel', '')
            
            return title, artist
            
    except Exception as e:
        logger.error(f"Error getting YouTube metadata: {e}")
        return None, None


def search_genius_lyrics(song_name: str, artist: str = "") -> Optional[str]:
    """
    Search Genius.com for lyrics.
    Note: Genius API requires token but we'll make it optional.
    
    Args:
        song_name: Song title
        artist: Artist name (optional)
        
    Returns:
        Lyrics text or None
    """
    try:
        import lyricsgenius
        import os
        
        # Try to get Genius token from environment
        token = os.getenv('GENIUS_ACCESS_TOKEN')
        
        if not token:
            # No token available - skip Genius search
            logger.info("No Genius API token - skipping Genius search")
            return None
        
        genius = lyricsgenius.Genius(token, timeout=15, retries=3, remove_section_headers=True)
        genius.verbose = False
        genius.remove_section_headers = True
        
        search_query = f"{artist} {song_name}" if artist else song_name
        
        song = genius.search_song(song_name, artist if artist else None)
        
        if song and song.lyrics:
            logger.info(f"Found lyrics on Genius for '{search_query}'")
            return song.lyrics
        
        logger.warning(f"No lyrics found on Genius for '{search_query}'")
        return None
        
    except Exception as e:
        logger.info(f"Genius search not available: {e}")
        return None


def search_lyrics_extractor(song_name: str, artist: str = "") -> Optional[str]:
    """
    Search for lyrics using direct web scraping from AZLyrics.
    Completely free, no API keys required.
    
    Args:
        song_name: Name of the song
        artist: Artist name (optional)
        
    Returns:
        Lyrics text or None
    """
    try:
        import requests
        from bs4 import BeautifulSoup
        import re
        
        if not artist:
            logger.warning("AZLyrics scraping requires artist name")
            return None
        
        # Clean artist and song names for URL
        def clean_for_url(text):
            # Remove special characters, keep only alphanumeric
            text = re.sub(r'[^a-z0-9]', '', text.lower())
            return text
        
        artist_clean = clean_for_url(artist)
        song_clean = clean_for_url(song_name)
        
        # AZLyrics URL format: https://www.azlyrics.com/lyrics/artist/song.html
        url = f"https://www.azlyrics.com/lyrics/{artist_clean}/{song_clean}.html"
        
        logger.info(f"Searching AZLyrics: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # AZLyrics puts lyrics in a div without a class, after a comment
            # Find all divs and look for the one with lyrics
            divs = soup.find_all('div', class_=False, id=False)
            
            for div in divs:
                text = div.get_text().strip()
                # Lyrics section is usually quite long
                if len(text) > 200 and '\n' in text:
                    logger.info(f"Found lyrics on AZLyrics ({len(text)} chars)")
                    return text
        
        logger.debug(f"No lyrics found on AZLyrics (status: {response.status_code})")
        return None
        
    except Exception as e:
        logger.debug(f"AZLyrics scraping failed: {e}")
        return None


def get_spotify_track_info(track_id: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Get track name and artist from Spotify.
    Note: Spotify API doesn't provide lyrics, just metadata.
    
    Returns:
        Tuple of (track_name, artist_name)
    """
    try:
        import spotipy
        from spotipy.oauth2 import SpotifyClientCredentials
        
        # Try without credentials first (limited functionality)
        sp = spotipy.Spotify()
        
        track = sp.track(track_id)
        track_name = track['name']
        artist_name = track['artists'][0]['name'] if track['artists'] else ''
        
        logger.info(f"Got Spotify metadata: {artist_name} - {track_name}")
        return track_name, artist_name
        
    except Exception as e:
        logger.warning(f"Spotify API error (may need credentials): {e}")
        return None, None


def get_lyrics_from_input(user_input: str) -> Tuple[Optional[str], str]:
    """
    Main function to get lyrics from user input.
    Handles URLs (YouTube, YouTube Music, Spotify) or song name search.
    
    Args:
        user_input: Either a URL or "Artist - Song Name" format
        
    Returns:
        Tuple of (lyrics_text, status_message)
    """
    user_input = user_input.strip()
    
    # Check if input is a YouTube URL
    if is_youtube_url(user_input):
        # For YouTube Music URLs, try scraping lyrics from the page first
        if is_youtube_music_url(user_input):
            logger.info(f"Detected YouTube Music URL, trying to scrape lyrics from page...")
            lyrics = get_youtube_music_lyrics(user_input)
            
            if lyrics:
                return lyrics, "✅ Extracted lyrics from YouTube Music page"
        
        # Extract video ID for fallback methods
        video_id = extract_video_id(user_input)
        if not video_id:
            return None, "❌ Could not extract video ID from YouTube URL"
        
        logger.info(f"Processing YouTube video ID: {video_id}")
        
        # Try to get subtitles using yt-dlp
        lyrics = get_youtube_subtitles_ytdlp(video_id)
        
        if lyrics:
            return lyrics, f"✅ Extracted captions from YouTube video: {video_id}"
        
        # If no subtitles, try to get video metadata and search for lyrics
        title, artist = get_youtube_metadata(video_id)
        
        if title:
            logger.info(f"No captions found. Searching for lyrics: {artist} - {title}")
            
            # Try Genius first
            lyrics = search_genius_lyrics(title, artist or "")
            if lyrics:
                return lyrics, f"✅ Found lyrics on Genius for: {artist} - {title}"
            
            # Try lyrics-extractor as fallback
            lyrics = search_lyrics_extractor(title, artist or "")
            if lyrics:
                return lyrics, f"✅ Found lyrics for: {artist} - {title}"
        
        return None, f"❌ No captions or lyrics found for video {video_id}"
    
    # Check if input is a Spotify URL
    elif is_spotify_url(user_input):
        track_id = extract_spotify_track_id(user_input)
        
        if not track_id:
            return None, "❌ Could not extract track ID from Spotify URL"
        
        logger.info(f"Processing Spotify track ID: {track_id}")
        
        # Get track metadata from Spotify (if available)
        track_name, artist_name = get_spotify_track_info(track_id)
        
        if track_name:
            logger.info(f"Found Spotify track: {artist_name} - {track_name}")
            
            # Search for lyrics using open-source methods
            lyrics = search_genius_lyrics(track_name, artist_name or "")
            if lyrics:
                return lyrics, f"✅ Found lyrics for: {artist_name} - {track_name}"
            
            lyrics = search_lyrics_extractor(track_name, artist_name or "")
            if lyrics:
                return lyrics, f"✅ Found lyrics for: {artist_name} - {track_name}"
            
            return None, f"❌ Found Spotify track '{artist_name} - {track_name}' but couldn't find lyrics"
        else:
            # Spotify metadata not available, inform user
            return None, "❌ Spotify requires authentication. Please use 'Artist - Song Name' format instead."
    
    # Assume it's a song name/artist search
    else:
        # Try to parse "Artist - Song Name" format
        if ' - ' in user_input:
            parts = user_input.split(' - ', 1)
            artist = parts[0].strip()
            song_name = parts[1].strip()
        else:
            artist = ""
            song_name = user_input
        
        logger.info(f"Searching for lyrics: {artist} - {song_name}")
        
        # Try Genius first
        lyrics = search_genius_lyrics(song_name, artist)
        if lyrics:
            return lyrics, f"✅ Found lyrics on Genius for: {user_input}"
        
        # Try AZLyrics as fallback
        lyrics = search_lyrics_extractor(song_name, artist)
        if lyrics:
            return lyrics, f"✅ Found lyrics for: {user_input}"
        
        return None, f"❌ Could not find lyrics for '{user_input}'. Try being more specific with 'Artist - Song Name' format."


if __name__ == "__main__":
    # Test
    test_inputs = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://music.youtube.com/watch?v=TzPfJbicPZc",
        "Radiohead - Karma Police",
    ]
    
    for inp in test_inputs:
        print(f"\n{'='*60}")
        print(f"Testing: {inp}")
        print('='*60)
        lyrics, status = get_lyrics_from_input(inp)
        print(status)
        if lyrics:
            print(f"Got {len(lyrics)} characters")
            print(f"Preview: {lyrics[:200]}...")
