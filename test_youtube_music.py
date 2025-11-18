"""Test YouTube Music link parsing and caption retrieval"""
from scraper import extract_video_id, get_youtube_captions, is_youtube_url

test_url = "https://music.youtube.com/watch?v=TzPfJbicPZc"

print(f"Testing URL: {test_url}")
print(f"Is YouTube URL: {is_youtube_url(test_url)}")

video_id = extract_video_id(test_url)
print(f"Extracted Video ID: {video_id}")

if video_id:
    print(f"\nTrying to get captions for video ID: {video_id}")
    lyrics = get_youtube_captions(video_id)
    
    if lyrics:
        print(f"✓ Success! Got {len(lyrics)} characters")
        print(f"First 200 chars: {lyrics[:200]}...")
    else:
        print("✗ No captions available for this video")
else:
    print("✗ Could not extract video ID")
