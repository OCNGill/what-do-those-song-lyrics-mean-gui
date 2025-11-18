"""Debug YouTube Music page structure"""
from playwright.sync_api import sync_playwright
import time

url = 'https://music.youtube.com/watch?v=kHvXvoXJu48'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    print(f"Loading: {url}")
    page.goto(url, wait_until='networkidle', timeout=45000)
    
    print("Waiting 8 seconds for page to fully load...")
    time.sleep(8)
    
    # Save screenshot
    page.screenshot(path='ytmusic_debug.png')
    print("Saved screenshot: ytmusic_debug.png")
    
    # Get all yt-formatted-string elements
    elements = page.locator('yt-formatted-string').all()
    print(f"\nFound {len(elements)} yt-formatted-string elements")
    
    for i, elem in enumerate(elements[:10]):
        try:
            text = elem.inner_text()
            classes = elem.get_attribute('class')
            if text and len(text) > 20:
                print(f"\nElement {i}:")
                print(f"  Classes: {classes}")
                print(f"  Text ({len(text)} chars): {text[:100]}...")
        except:
            pass
    
    print("\n\nPress Ctrl+C to close...")
    try:
        time.sleep(300)
    except KeyboardInterrupt:
        pass
    
    browser.close()
