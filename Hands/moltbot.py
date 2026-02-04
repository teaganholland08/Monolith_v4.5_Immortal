"""
THE HAND - Browser Control Engine (v2.0)
Capability: Web automation and scraping
Engine: PLAYWRIGHT (Best in World Standard)
Status: PRODUCTION READY
"""

import sys
import os
import time
import logging
from typing import Optional, Dict, Any

# Add parent dir to path to find config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    import config
except ImportError:
    pass

try:
    from playwright.sync_api import sync_playwright, Page, Browser, Playwright
except ImportError:
    print("❌ PLAYWRIGHT NOT INSTALLED. Run: pip install playwright && playwright install")

class Moltbot:
    """
    The autonomous browser agent for Project Monolith.
    Uses Playwright for maximum stealth and speed.
    """
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.setup_driver()

    def setup_driver(self):
        """Initialize Playwright Engine"""
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                args=["--disable-blink-features=AutomationControlled"] # Basic stealth
            )
            context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            )
            self.page = context.new_page()
            print(f"🌍 MOLTBOT: Playwright Engine Initialized (Headless: {self.headless})")
        except Exception as e:
            print(f"❌ MOLTBOT ERROR: Failed to start Playwright. {e}")

    def browse(self, url: str) -> str:
        """Navigate to a URL and return page content"""
        # CONFIG CHECK
        if 'config' in sys.modules and getattr(config, 'USE_SIMULATION_MODE', False):
             print(f"🌍 [SIMULATION] Visiting {url}")
             return f"<html><body>Mock Content from {url}</body></html>"

        if not self.page:
            return "Error: Browser not initialized"

        try:
            print(f"🌍 NAVIGATING: {url}")
            self.page.goto(url, wait_until="domcontentloaded")
            # Wait for human-like loading
            time.sleep(2) 
            return self.page.content()
        except Exception as e:
            print(f"❌ ERROR Visiting {url}: {e}")
            return ""

    def click(self, selector: str):
        """Click an element securely"""
        if not self.page: return
        try:
            print(f"🖱️ CLICKING: {selector}")
            self.page.click(selector)
            time.sleep(1)
        except Exception as e:
            print(f"❌ CLICK ERROR: {e}")

    def type_text(self, selector: str, text: str):
        """Type text into a field"""
        if not self.page: return
        try:
            print(f"⌨️ TYPING: '{text}' into {selector}")
            self.page.fill(selector, text)
        except Exception as e:
            print(f"❌ TYPE ERROR: {e}")

    def scrape_text(self, url: str, selector: str) -> str:
        """Extract text from a specific element"""
        if 'config' in sys.modules and getattr(config, 'USE_SIMULATION_MODE', False):
            return "Mock Scraped Text"
            
        if not self.page:
            self.setup_driver()
        
        try:
            if self.page.url != url:
                self.browse(url)
                
            element = self.page.wait_for_selector(selector, timeout=10000)
            if element:
                return element.inner_text()
            return ""
        except Exception as e:
            print(f"❌ SCRAPE ERROR: {e}")
            return ""

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

# Standalone Usage
if __name__ == "__main__":
    if len(sys.argv) > 1:
        bot = Moltbot(headless=False)
        print(bot.browse(sys.argv[1]))
        bot.close()
    else:
        print("Usage: python moltbot.py <url>")
