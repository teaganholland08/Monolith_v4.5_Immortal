"""
MONOLITH INTELLIGENCE LAYER - News Scanner
Environmental Scanning & OSINT Module

Monitors 24/7 for:
- Breaking news (global events)
- Tax law changes
- Regulatory updates
- Market sentiment shifts
- Technology trends
"""

import requests
import os
import time
from datetime import datetime

class NewsScanner:
    def __init__(self):
        self.api_key = os.getenv("NEWSAPI_KEY", "")  # Get free key at newsapi.org
        self.sources = {
            "news": "https://newsapi.org/v2/top-headlines",
            "reddit": "https://www.reddit.com/r/technology/hot.json",
            "congress": "https://api.congress.gov/v3/bill",
        }
        self.keywords = [
            "tax", "crypto", "regulation", "AI", "loophole", 
            "exemption", "privacy", "offshore", "LLC"
        ]
        
    def scan_global_news(self):
        """Fetch breaking news from major sources"""
        if not self.api_key:
            print("   ⚠️ NEWS SCANNER: No API key. Set NEWSAPI_KEY env variable.")
            return []
        
        try:
            response = requests.get(
                self.sources["news"],
                params={
                    "apiKey": self.api_key,
                    "language": "en",
                    "pageSize": 20
                },
                timeout=10
            )
            articles = response.json().get("articles", [])
            return self._filter_relevant(articles)
        except Exception as e:
            print(f"   ⚠️ NEWS API ERROR: {e}")
            return []
    
    def scan_reddit_sentiment(self):
        """Monitor Reddit for emerging trends"""
        try:
            headers = {"User-Agent": "Monolith/1.0"}
            response = requests.get(
                self.sources["reddit"],
                headers=headers,
                timeout=10
            )
            posts = response.json().get("data", {}).get("children", [])
            
            hot_topics = []
            for post in posts[:10]:
                data = post.get("data", {})
                title = data.get("title", "")
                if any(kw in title.lower() for kw in self.keywords):
                    hot_topics.append({
                        "title": title,
                        "score": data.get("score", 0),
                        "url": f"https://reddit.com{data.get('permalink', '')}"
                    })
            return hot_topics
        except Exception as e:
            print(f"   ⚠️ REDDIT SCAN ERROR: {e}")
            return []
    
    def _filter_relevant(self, articles):
        """Filter news for money-making opportunities"""
        relevant = []
        for article in articles:
            title = article.get("title", "").lower()
            description = article.get("description", "").lower()
            
            if any(kw in title or kw in description for kw in self.keywords):
                relevant.append({
                    "headline": article.get("title"),
                    "summary": article.get("description"),
                    "source": article.get("source", {}).get("name"),
                    "url": article.get("url")
                })
        return relevant
    
    def run_scan_cycle(self):
        """Execute full intelligence sweep"""
        print("   📡 INTELLIGENCE: Scanning global information stream...")
        
        news = self.scan_global_news()
        reddit = self.scan_reddit_sentiment()
        
        signals = []
        
        for item in news:
            signals.append({
                "type": "NEWS",
                "content": item["headline"],
                "source": item["source"],
                "url": item["url"],
                "timestamp": datetime.now().isoformat()
            })
        
        for topic in reddit:
            if topic["score"] > 1000:  # High visibility
                signals.append({
                    "type": "REDDIT_TREND",
                    "content": topic["title"],
                    "score": topic["score"],
                    "url": topic["url"],
                    "timestamp": datetime.now().isoformat()
                })
        
        return signals

if __name__ == "__main__":
    scanner = NewsScanner()
    signals = scanner.run_scan_cycle()
    
    print(f"\n🎯 DETECTED {len(signals)} SIGNALS:")
    for sig in signals[:5]:  # Show top 5
        print(f"   [{sig['type']}] {sig['content'][:80]}...")
