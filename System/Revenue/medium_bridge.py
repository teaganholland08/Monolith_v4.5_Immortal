"""
MONOLITH REVENUE BRIDGE - Medium Partner Program Integration
Auto-publishes Genesis Engine articles to Medium for passive income

Revenue Model:
- Medium pays $0.05 - $2.00 per read (Member reads)
- Viral article (10k reads) = $500 - $2,000
- 10 articles/month at 500 reads = $250 - $500/month

Setup:
1. Create Medium account at medium.com
2. Apply for Medium Partner Program
3. Get Integration Token: Settings > Security > Integration tokens
4. Set env variable: MEDIUM_INTEGRATION_TOKEN
"""

import requests
import os
from pathlib import Path
from datetime import datetime

class MediumBridge:
    def __init__(self):
        self.token = os.getenv("MEDIUM_INTEGRATION_TOKEN", "")
        self.base_url = "https://api.medium.com/v1"
        self.user_id = None
        
    def is_configured(self):
        """Check if API token is set"""
        return bool(self.token)
    
    def get_user_id(self):
        """Fetch authenticated user's ID"""
        if self.user_id:
            return self.user_id
        
        if not self.is_configured():
            return None
        
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(
                f"{self.base_url}/me",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                self.user_id = response.json().get("data", {}).get("id")
                return self.user_id
        except:
            return None
    
    def publish_article(self, title, content, tags=None):
        """
        Publish article to Medium
        
        Args:
            title: Article headline
            content: Markdown or HTML content
            tags: List of tags (max 5)
        
        Returns:
            dict with url, status, message
        """
        if not self.is_configured():
            return {
                "status": "ERROR",
                "message": "MEDIUM_INTEGRATION_TOKEN not set"
            }
        
        user_id = self.get_user_id()
        if not user_id:
            return {
                "status": "ERROR",
                "message": "Cannot fetch user ID (check token)"
            }
        
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "title": title,
                "contentFormat": "markdown",
                "content": content,
                "publishStatus": "public",
                "tags": tags or []
            }
            
            response = requests.post(
                f"{self.base_url}/users/{user_id}/posts",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 201:
                data = response.json().get("data", {})
                return {
                    "status": "SUCCESS",
                    "url": data.get("url"),
                    "id": data.get("id"),
                    "message": f"Published: {data.get('url')}"
                }
            else:
                return {
                    "status": "ERROR",
                    "message": f"API error: {response.text}"
                }
        
        except Exception as e:
            return {
                "status": "ERROR",
                "message": str(e)
            }
    
    def auto_publish_genesis_article(self, markdown_file_path):
        """
        Automatically publish Genesis-generated markdown as Medium article
        
        Extracts title from first H1 heading
        Auto-tags based on content
        """
        file_path = Path(markdown_file_path)
        
        if not file_path.exists():
            return {"status": "ERROR", "message": "File not found"}
        
        if file_path.suffix != ".md":
            return {"status": "SKIPPED", "message": "Not a markdown file"}
        
        # Read content
        content = file_path.read_text(encoding='utf-8')
        
        # Extract title (first # heading)
        lines = content.split('\n')
        title = None
        for line in lines:
            if line.startswith('# '):
                title = line[2:].strip()
                break
        
        if not title:
            title = file_path.stem.replace('_', ' ').title()
        
        # Auto-generate tags
        tags = []
        if "tax" in content.lower():
            tags.append("tax-optimization")
        if "crypto" in content.lower() or "bitcoin" in content.lower():
            tags.append("cryptocurrency")
        if "python" in content.lower() or "code" in content.lower():
            tags.append("programming")
        if "ai" in content.lower():
            tags.append("artificial-intelligence")
        tags.append("automation")  # Always include
        
        # Publish
        result = self.publish_article(title, content, tags[:5])
        
        # Log if successful
        if result.get("status") == "SUCCESS":
            self._log_publication(title, result.get("url"))
        
        return result
    
    def _log_publication(self, title, url):
        """Log article to tracking file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "title": title,
            "url": url,
            "platform": "Medium"
        }
        
        log_file = Path(__file__).parent.parent / "Logs" / "medium_articles.log"
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(f"{log_entry}\n")
    
    def get_stats(self):
        """Fetch publication stats (requires separate API call)"""
        # Medium API doesn't provide analytics directly
        # Would need to scrape or use third-party analytics
        return {
            "note": "Medium stats require Medium Partner Dashboard access",
            "dashboard_url": "https://medium.com/me/stats"
        }

if __name__ == "__main__":
    bridge = MediumBridge()
    
    if not bridge.is_configured():
        print("⚠️ MEDIUM SETUP REQUIRED")
        print("\n1. Go to: https://medium.com/me/settings/security")
        print("2. Under 'Integration tokens', create new token")
        print("3. Set environment variable:")
        print('   setx MEDIUM_INTEGRATION_TOKEN "your_token_here"')
        print("\n4. Apply for Medium Partner Program:")
        print("   https://medium.com/creators")
        print("\nThen restart terminal and run again.")
    else:
        print("✓ Medium configured")
        user_id = bridge.get_user_id()
        if user_id:
            print(f"✓ User ID: {user_id}")
        else:
            print("⚠️ Cannot fetch user (check token)")
