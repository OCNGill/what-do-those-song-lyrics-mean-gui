"""Test updated scraper with multiple sources"""
from scraper_v2 import get_lyrics_from_input

tests = [
    ("YouTube Music", "https://music.youtube.com/watch?v=kHvXvoXJu48"),
    ("Artist - Song search", "Pink Floyd - Time"),
    ("YouTube with subtitles", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
]

print("=" * 70)
print("TESTING UPDATED SCRAPER WITH OPEN-SOURCE METHODS")
print("=" * 70)

for name, query in tests:
    print(f"\n[{name}]")
    print(f"Query: {query}")
    print("-" * 70)
    
    lyrics, status = get_lyrics_from_input(query)
    
    print(status)
    if lyrics:
        print(f"Got {len(lyrics)} characters")
        print(f"Preview: {lyrics[:150]}...")
    else:
        print("No lyrics found")
    
    print()
