"""Test scraping lyrics from YouTube Music page using Playwright"""
from playwright.sync_api import sync_playwright
import time

url = 'https://music.youtube.com/watch?v=kHvXvoXJu48'

print(f"Opening: {url}")
print("=" * 60)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set to False to see what's happening
    page = browser.new_page()
    
    try:
        # Navigate to the page
        page.goto(url, wait_until='networkidle', timeout=30000)
        
        # Wait a bit for dynamic content to load
        time.sleep(3)
        
        # Look for lyrics tab/button
        print("Looking for LYRICS tab...")
        
        # Try to find and click the Lyrics tab
        try:
            lyrics_tab = page.locator('text=LYRICS').first
            if lyrics_tab.is_visible():
                print("Found LYRICS tab, clicking...")
                lyrics_tab.click()
                time.sleep(2)
        except:
            print("Could not find or click LYRICS tab")
        
        # Try different selectors for lyrics content
        selectors = [
            'ytmusic-description-shelf-renderer',
            '[class*="description"]',
            '[class*="lyrics"]',
            'yt-formatted-string.description',
        ]
        
        for selector in selectors:
            print(f"\nTrying selector: {selector}")
            elements = page.locator(selector).all()
            print(f"Found {len(elements)} elements")
            
            for i, elem in enumerate(elements[:3]):  # Check first 3
                try:
                    text = elem.inner_text()
                    if text and len(text) > 50:
                        print(f"\nElement {i} text (first 200 chars):")
                        print(text[:200])
                        print(f"Total length: {len(text)}")
                except:
                    pass
        
        # Get the full page content to inspect
        print("\n\nPage title:", page.title())
        
        input("\n\nPress Enter to close browser...")
        
    finally:
        browser.close()
