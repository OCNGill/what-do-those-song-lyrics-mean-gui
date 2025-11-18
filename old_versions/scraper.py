"""
Scraper module for extracting lyrics from YouTube, YouTube Music, and Spotify.
Uses youtube-transcript-api for captions and Playwright for search functionality.
"""
from __future__ import annotations

import logging
import re
from typing import Optional
from urllib.parse import parse_qs, urlparse

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import (
        NoTranscriptFound,
        TranscriptsDisabled,
        VideoUnavailable,
    )
except ImportError:
    # Fallback for older versions
    from youtube_transcript_api import YouTubeTranscriptApi
    NoTranscriptFound = Exception
    TranscriptsDisabled = Exception
    VideoUnavailable = Exception

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
        if 'youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc:
            query_params = parse_qs(parsed.query)
            if 'v' in query_params:
                return query_params['v'][0]
    except Exception as e:
        logger.error(f"Error parsing URL: {e}")
    
    return None


def is_youtube_url(text: str) -> bool:
    """Check if the input text is a YouTube or YouTube Music URL."""
    youtube_domains = ['youtube.com', 'youtu.be', 'music.youtube.com']
    return any(domain in text.lower() for domain in youtube_domains)


def is_spotify_url(text: str) -> bool:
    """Check if the input text is a Spotify URL."""
    return 'spotify.com' in text.lower()


def get_youtube_captions(video_id: str) -> Optional[str]:
    """
    Retrieve captions/subtitles from a YouTube video.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Concatenated transcript text or None if unavailable
    """
    try:
        # Get transcript directly (simpler API call)
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US'])
        
        # Concatenate all transcript segments
        full_text = ' '.join([entry['text'] for entry in transcript_data])
        
        # Clean up the text
        full_text = full_text.replace('\n', ' ').strip()
        
        logger.info(f"Successfully retrieved captions for video ID: {video_id}")
        return full_text
        
    except Exception as e:
        # Try to get any available transcript if English fails
        try:
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
            full_text = ' '.join([entry['text'] for entry in transcript_data])
            full_text = full_text.replace('\n', ' ').strip()
            logger.info(f"Retrieved non-English captions for video ID: {video_id}")
            return full_text
        except Exception as e2:
            logger.error(f"Error retrieving captions: {e}")
            return None


def search_youtube_for_song(song_name: str, artist: str = "") -> Optional[str]:
    """
    Search YouTube for a song and return the first result's video ID.
    
    Args:
        song_name: Name of the song
        artist: Artist name (optional but recommended)
        
    Returns:
        Video ID of the first search result, or None if not found
    """
    try:
        from playwright.sync_api import sync_playwright
        
        search_query = f"{artist} {song_name} lyrics" if artist else f"{song_name} lyrics"
        search_url = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(search_url, wait_until='domcontentloaded', timeout=15000)
            
            # Wait for search results to load
            page.wait_for_selector('a#video-title', timeout=10000)
            
            # Get the first video link
            first_video = page.query_selector('a#video-title')
            if first_video:
                href = first_video.get_attribute('href')
                browser.close()
                
                if href:
                    # Extract video ID from href
                    video_id = extract_video_id(f"https://www.youtube.com{href}")
                    logger.info(f"Found video ID for '{search_query}': {video_id}")
                    return video_id
            
            browser.close()
            logger.warning(f"No video found for search: {search_query}")
            return None
            
    except Exception as e:
        logger.error(f"Error searching YouTube: {e}")
        return None


def get_lyrics_from_input(user_input: str) -> tuple[Optional[str], str]:
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
        video_id = extract_video_id(user_input)
        if not video_id:
            return None, "❌ Could not extract video ID from YouTube URL"
        
        lyrics = get_youtube_captions(video_id)
        if lyrics:
            return lyrics, f"✅ Successfully extracted captions from YouTube video: {video_id}"
        else:
            return None, "❌ No captions available for this YouTube video"
    
    # Check if input is a Spotify URL
    elif is_spotify_url(user_input):
        # For Spotify, we'll need to extract song info and search YouTube
        return None, "⚠️ Spotify URL detected. Please try searching with 'Artist - Song Name' instead, as Spotify links don't contain lyrics directly."
    
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
        
        # Search YouTube
        video_id = search_youtube_for_song(song_name, artist)
        if not video_id:
            return None, f"❌ Could not find '{user_input}' on YouTube"
        
        # Get captions from found video
        lyrics = get_youtube_captions(video_id)
        if lyrics:
            return lyrics, f"✅ Found and extracted lyrics for '{user_input}' (Video ID: {video_id})"
        else:
            return None, f"❌ Found video for '{user_input}' but no captions available"
