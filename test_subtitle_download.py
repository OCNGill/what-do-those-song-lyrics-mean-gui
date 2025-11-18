"""Test downloading and parsing subtitle"""
import requests
import yt_dlp
from bs4 import BeautifulSoup

video_id = "dQw4w9WgXcQ"
url = f"https://www.youtube.com/watch?v={video_id}"

# Get subtitle URL
ydl_opts = {'skip_download': True, 'writesubtitles': True, 'subtitleslangs': ['en'], 'quiet': True}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    
    # Try manual subtitles first
    subs = info.get('subtitles', {}).get('en', [])
    if not subs:
        subs = info.get('automatic_captions', {}).get('en', [])
    
    if subs:
        # Find srv3 format (XML)
        sub_url = None
        for s in subs:
            if s.get('ext') == 'srv3':
                sub_url = s.get('url')
                break
        
        if not sub_url:
            # Fallback to first available
            sub_url = subs[0].get('url')
        
        print(f"Downloading from: {sub_url[:100]}...")
        
        response = requests.get(sub_url, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Content length: {len(response.content)}")
        print(f"Content type: {response.headers.get('content-type')}")
        print(f"\nFirst 500 chars of content:\n{response.text[:500]}")
        
        # Try parsing
        print("\n--- Parsing with lxml ---")
        soup = BeautifulSoup(response.content, 'lxml')
        print(f"Soup type: {type(soup)}")
        
        # Try different tag names
        for tag in ['text', 'p', 's']:
            elements = soup.find_all(tag)
            print(f"Found {len(elements)} <{tag}> elements")
            if elements:
                print(f"First element: {elements[0]}")
                break
