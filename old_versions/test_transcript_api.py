"""Test YouTube transcript API directly"""
from youtube_transcript_api import YouTubeTranscriptApi

# Test with known videos that have captions
test_videos = [
    ("dQw4w9WgXcQ", "Rick Astley - Never Gonna Give You Up"),
    ("9bZkp7q19f0", "PSY - Gangnam Style"),
    ("kJQP7kiw5Fk", "Luis Fonsi - Despacito"),
]

print("Testing YouTube Transcript API...")
print("="*60)

for video_id, title in test_videos:
    print(f"\nTesting: {title}")
    print(f"Video ID: {video_id}")
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        print(f"✓ Success! Got {len(transcript)} segments")
        if transcript:
            first_text = transcript[0]['text'][:50]
            print(f"  First text: {first_text}...")
    except Exception as e:
        print(f"✗ Failed: {e}")

print("\n" + "="*60)
print("Testing YouTube Music URL...")
yt_music_id = "TzPfJbicPZc"
try:
    transcript = YouTubeTranscriptApi.get_transcript(yt_music_id)
    print(f"✓ Video {yt_music_id}: Got {len(transcript)} segments")
except Exception as e:
    print(f"✗ Video {yt_music_id}: {e}")
