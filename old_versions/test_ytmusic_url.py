"""Test YouTube Music URL"""
from scraper_v2 import get_lyrics_from_input

url = 'https://music.youtube.com/watch?v=kHvXvoXJu48'
print(f"Testing: {url}")
print("=" * 60)

result = get_lyrics_from_input(url)

if result and len(result) > 100:
    print(f"✅ SUCCESS! Got {len(result)} characters")
    print(f"\nFirst 500 characters:")
    print(result[:500])
else:
    print(f"❌ FAILED - No lyrics found")
    print(f"Result: {result}")
