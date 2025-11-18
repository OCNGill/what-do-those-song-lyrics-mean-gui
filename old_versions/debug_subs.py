"""Debug subtitle download"""
import yt_dlp

video_id = "dQw4w9WgXcQ"
url = f"https://www.youtube.com/watch?v={video_id}"

ydl_opts = {
    'skip_download': True,
    'writesubtitles': True,
    'writeautomaticsub': True,
    'subtitleslangs': ['en'],
    'quiet': False,
}

print(f"Getting info for: {url}")

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    
    print(f"\nTitle: {info.get('title')}")
    print(f"Uploader: {info.get('uploader')}")
    
    if 'subtitles' in info:
        print(f"\nManual subtitles available: {list(info['subtitles'].keys())}")
        if 'en' in info['subtitles']:
            print(f"English subtitle formats: {len(info['subtitles']['en'])}")
            for sub in info['subtitles']['en']:
                print(f"  - {sub.get('ext')}: {sub.get('url')[:80]}...")
    
    if 'automatic_captions' in info:
        print(f"\nAuto captions available: {list(info['automatic_captions'].keys())}")
        if 'en' in info['automatic_captions']:
            print(f"English auto-caption formats: {len(info['automatic_captions']['en'])}")
            for sub in info['automatic_captions']['en']:
                print(f"  - {sub.get('ext')}: {sub.get('url')[:80]}...")
