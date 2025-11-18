"""Test YouTube Music lyrics scraping"""
from scraper_v2 import get_lyrics_from_input

url = 'https://music.youtube.com/watch?v=kHvXvoXJu48'
print(f"Testing: {url}")
print("=" * 60)

lyrics, status = get_lyrics_from_input(url)

print(status)
if lyrics:
    print(f"\n✅ SUCCESS! Got {len(lyrics)} characters")
    print(f"\nFirst 300 characters:")
    print(lyrics[:300])
    print("...")
else:
    print("\n❌ FAILED")
