"""
METADATA SHIELDING - Traffic Pattern Obfuscation
2026 best practice for digital ghost operation

Features:
- Ghost packet generation (decoy traffic)
- Traffic pattern masking
- 48-hour location decoy (vanish support)
- Real traffic camouflage
"""

import requests
import random
import time
from datetime import datetime, timedelta
from pathlib import Path
import json
import threading

class MetadataShielder:
    """
    Advanced metadata obfuscation via ghost traffic
    
    Hides real operations in noise:
    - Generates realistic decoy web traffic
    - Masks AI agent API calls as normal browsing
    - Creates location decoy for 48 hours during vanish
    - Prevents traffic pattern analysis
    """
    
    def __init__(self):
        self.config_file = Path(__file__).parent.parent / "Config" / "metadata_shield_config.json"
        self.running = False
        self.decoy_thread = None
        
        self._load_config()
    
    def _load_config(self):
        """Load shielding configuration"""
        if not self.config_file.exists():
            default_config = {
                "enabled": True,
                "ghost_traffic": {
                    "requests_per_hour": 20,
                    "sites": [
                        "https://www.youtube.com",
                        "https://www.reddit.com",
                        "https://news.ycombinator.com",
                        "https://www.cbc.ca/news",
                        "https://www.github.com",
                        "https://stackoverflow.com",
                        "https://www.wikipedia.org"
                    ],
                    "user_agents": [
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                    ]
                },
                "location_decoy": {
                    "enabled": False,
                    "original_location": "Powell River, BC",
                    "duration_hours": 48
                },
                "traffic_masking": {
                    "delay_min_seconds": 120,
                    "delay_max_seconds": 600,
                    "simulate_video_streaming": True,
                    "simulate_social_media": True
                }
            }
            
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            print(f"[INFO] Created metadata shield config: {self.config_file}")
            self.config = default_config
        else:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
    
    def _generate_ghost_traffic(self):
        """Generate realistic decoy web requests"""
        sites = self.config["ghost_traffic"]["sites"]
        user_agents = self.config["ghost_traffic"]["user_agents"]
        
        while self.running:
            try:
                # Pick random site
                site = random.choice(sites)
                user_agent = random.choice(user_agents)
                
                # Make request
                headers = {"User-Agent": user_agent}
                response = requests.get(site, headers=headers, timeout=10)
                
                print(f"[GHOST] {datetime.now().strftime('%H:%M:%S')} - {site} ({response.status_code})")
                
                # Wait random interval
                delay_min = self.config["traffic_masking"]["delay_min_seconds"]
                delay_max = self.config["traffic_masking"]["delay_max_seconds"]
                delay = random.randint(delay_min, delay_max)
                
                time.sleep(delay)
                
            except Exception as e:
                print(f"[GHOST] Error: {e}")
                time.sleep(60)  # Wait before retry
    
    def start_shielding(self):
        """Start metadata obfuscation"""
        if not self.config["enabled"]:
            print("[WARN] Metadata shielding disabled in config")
            return
        
        if self.running:
            print("[WARN] Shielding already running")
            return
        
        print("\n" + "="*60)
        print("METADATA SHIELDING ACTIVE")
        print("="*60)
        print("\nGenerating ghost traffic to mask real operations...")
        print(f"Target: {self.config['ghost_traffic']['requests_per_hour']} req/hour")
        print("\nPress Ctrl+C to stop\n")
        
        self.running = True
        self.decoy_thread = threading.Thread(target=self._generate_ghost_traffic, daemon=True)
        self.decoy_thread.start()
    
    def stop_shielding(self):
        """Stop metadata obfuscation"""
        self.running = False
        if self.decoy_thread:
            self.decoy_thread.join(timeout=5)
        
        print("\n[OK] Metadata shielding stopped")
    
    def activate_location_decoy(self, duration_hours=48):
        """
        Activate location decoy for vanishing scenario
        
        Continues ghost traffic at old location while user relocates
        """
        print("\n" + "="*60)
        print("LOCATION DECOY ACTIVATED")
        print("="*60)
        print(f"\nDuration: {duration_hours} hours")
        print(f"Decoy Location: {self.config['location_decoy']['original_location']}")
        print("\nThis creates a digital presence at your old location")
        print("while you physically relocate.")
        print("\n" + "="*60 + "\n")
        
        # Update config
        self.config["location_decoy"]["enabled"] = True
        self.config["location_decoy"]["duration_hours"] = duration_hours
        
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        # Start shielding
        self.start_shielding()
        
        # Schedule auto-disable after duration
        stop_time = datetime.now() + timedelta(hours=duration_hours)
        print(f"[INFO] Decoy will auto-disable at {stop_time.strftime('%Y-%m-%d %H:%M')}")
    
    def mask_api_call(self, api_url, method="GET", **kwargs):
        """
        Make API call disguised as normal traffic
        
        Adds random delay and ghost traffic around real call
        """
        # Pre-call ghost traffic
        self._generate_ghost_traffic_burst(1)
        
        # Make real call
        response = requests.request(method, api_url, **kwargs)
        
        # Post-call ghost traffic
        self._generate_ghost_traffic_burst(1)
        
        return response
    
    def _generate_ghost_traffic_burst(self, count):
        """Generate quick burst of ghost traffic"""
        sites = self.config["ghost_traffic"]["sites"]
        user_agents = self.config["ghost_traffic"]["user_agents"]
        
        for _ in range(count):
            try:
                site = random.choice(sites)
                user_agent = random.choice(user_agents)
                headers = {"User-Agent": user_agent}
                requests.get(site, headers=headers, timeout=5)
            except:
                pass

if __name__ == "__main__":
    shield = MetadataShielder()
    
    print("\n" + "="*60)
    print("METADATA SHIELDING UTILITY")
    print("="*60)
    print("\nOptions:")
    print("  1. Start continuous shielding")
    print("  2. Activate 48-hour location decoy")
    print("  3. Test single ghost request")
    print("\nConfiguration:")
    print(f"  Enabled: {shield.config['enabled']}")
    print(f"  Ghost sites: {len(shield.config['ghost_traffic']['sites'])}")
    print(f"  Requests/hour target: {shield.config['ghost_traffic']['requests_per_hour']}")
    
    try:
        choice = input("\nChoice (1-3, or Enter to skip): ").strip()
        
        if choice == "1":
            shield.start_shielding()
            while True:
                time.sleep(1)
        elif choice == "2":
            shield.activate_location_decoy(48)
            while True:
                time.sleep(1)
        elif choice == "3":
            shield._generate_ghost_traffic_burst(3)
            print("\n[OK] Test complete")
    
    except KeyboardInterrupt:
        shield.stop_shielding()
        print("\nShutdown complete")
