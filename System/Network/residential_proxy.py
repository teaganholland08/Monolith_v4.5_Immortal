"""
RESIDENTIAL PROXY ROTATION
2026 best practices for stealth web access

Features:
- Proxy rotation (residential IPs)
- Rate limiting per IP
- Health monitoring
- Automatic fallback
"""

import requests
from pathlib import Path
import json
import time
from datetime import datetime, timedelta

class ResidentialProxy:
    """
    Residential proxy manager for stealth operations
    
    Prevents:
    - IP bans from scraping
    - Rate limiting
    - Geographic restrictions
    - Tracking across sessions
    """
    
    def __init__(self):
        self.config_file = Path(__file__).parent.parent / "Config" / "proxy_config.json"
        self.proxies = []
        self.current_index = 0
        self.request_counts = {}
        
        self._load_config()
    
    def _load_config(self):
        """Load proxy configuration"""
        if not self.config_file.exists():
            # Create default config
            default_config = {
                "providers": {
                    "brightdata": {
                        "enabled": False,
                        "username": "",
                        "password": "",
                        "endpoint": "brd.superproxy.io:22225"
                    },
                    "smartproxy": {
                        "enabled": False,
                        "username": "",
                        "password": "",
                        "endpoint": "gate.smartproxy.com:7000"
                    },
                    "oxylabs": {
                        "enabled": False,
                        "username": "",
                        "password": "",
                        "endpoint": "pr.oxylabs.io:7777"
                    }
                },
                "rotation": {
                    "max_requests_per_ip": 50,
                    "cooldown_seconds": 300
                }
            }
            
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            print(f"[INFO] Created proxy config: {self.config_file}")
            print("[INFO] Configure proxy providers in config file")
            
            self.config = default_config
        else:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        
        # Build proxy list from enabled providers
        for provider, settings in self.config["providers"].items():
            if settings["enabled"]:
                proxy_url = f"http://{settings['username']}:{settings['password']}@{settings['endpoint']}"
                self.proxies.append({
                    "provider": provider,
                    "url": proxy_url,
                    "last_used": None,
                    "requests_made": 0
                })
    
    def get_proxy(self):
        """
        Get next available proxy with rotation
        
        Returns: Dict with http/https proxy URLs
        """
        if not self.proxies:
            print("[WARN] No proxies configured, using direct connection")
            return None
        
        max_requests = self.config["rotation"]["max_requests_per_ip"]
        cooldown = self.config["rotation"]["cooldown_seconds"]
        
        # Find available proxy
        for _ in range(len(self.proxies)):
            proxy = self.proxies[self.current_index]
            
            # Check if proxy is available
            now = datetime.now()
            
            if proxy["last_used"]:
                time_since_use = (now - proxy["last_used"]).total_seconds()
                
                # Reset counter if cooldown passed
                if time_since_use > cooldown:
                    proxy["requests_made"] = 0
            
            # Check request limit
            if proxy["requests_made"] < max_requests:
                # Use this proxy
                proxy["last_used"] = now
                proxy["requests_made"] += 1
                
                self.current_index = (self.current_index + 1) % len(self.proxies)
                
                return {
                    "http": proxy["url"],
                    "https": proxy["url"]
                }
            
            # Try next proxy
            self.current_index = (self.current_index + 1) % len(self.proxies)
        
        # All proxies exhausted
        print("[WARN] All proxies at request limit, using direct connection")
        return None
    
    def test_proxy(self, proxy_dict):
        """Test if proxy is working"""
        try:
            response = requests.get(
                "https://api.ipify.org/?format=json",
                proxies=proxy_dict,
                timeout=10
            )
            
            if response.status_code == 200:
                ip = response.json()["ip"]
                print(f"[OK] Proxy working, IP: {ip}")
                return True
            else:
                print(f"[FAIL] Proxy returned status {response.status_code}")
                return False
                
        except Exception as e:
            print(f"[FAIL] Proxy test failed: {e}")
            return False
    
    def make_request(self, url, method="GET", **kwargs):
        """
        Make HTTP request with automatic proxy rotation
        
        Args:
            url: Target URL
            method: HTTP method (GET, POST, etc.)
            **kwargs: Additional requests arguments
        
        Returns: requests.Response object
        """
        proxy = self.get_proxy()
        
        if proxy:
            kwargs["proxies"] = proxy
        
        # Add user agent if not provided
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        
        if "User-Agent" not in kwargs["headers"]:
            kwargs["headers"]["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        
        # Make request
        return requests.request(method, url, **kwargs)

if __name__ == "__main__":
    proxy_mgr = ResidentialProxy()
    
    print("\n" + "="*60)
    print("RESIDENTIAL PROXY MANAGER")
    print("="*60)
    
    if proxy_mgr.proxies:
        print(f"\nConfigured proxies: {len(proxy_mgr.proxies)}")
        
        # Test first proxy
        test_proxy = proxy_mgr.get_proxy()
        if test_proxy:
            print("\nTesting proxy...")
            proxy_mgr.test_proxy(test_proxy)
    else:
        print("\nNo proxies configured.")
        print(f"Edit: {proxy_mgr.config_file}")
        print("\nRecommended providers (2026):")
        print("  - Bright Data (residential IPs, 72M+ pool)")
        print("  - SmartProxy (40M+ IPs, rotating)")
        print("  - Oxylabs (100M+ IPs, premium)")
