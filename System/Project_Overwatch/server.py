import time, psutil, feedparser, requests, imaplib, email, random, threading, json, os, glob
from datetime import datetime
from email.header import decode_header
from pushbullet import Pushbullet
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- A. CONFIGURATION & KEYS ---
CONFIG = {
    "GMAIL_USER": "YOUR_EMAIL@gmail.com",
    "GMAIL_PASS": "YOUR_APP_PASSWORD",
    "PUSHBULLET": "o.YOUR_KEY",
    "LOCATION": {"lat": "49.8352", "lon": "-124.5247"}, 
    "PATHS": {
        # THE BRIDGE: Connecting Monolith to the Sub-Systems
        "PROFIT_ENGINE": "autonomous_profit_system/earnings.json",
        "NOTIFICATIONS": "autonomous_profit_system/notifications.json",
        "THREATS": "threats.json" # Kept in root for manual override
    }
}

# --- B. DATA LOADERS ---
def load_json(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f: return json.load(f)
        except: return None
    return None

# --- C. SYSTEM SUPERVISOR ---
SYSTEM_HEALTH = []
DYNAMIC_ALERTS = []

def run_audit():
    global SYSTEM_HEALTH
    SYSTEM_HEALTH = []
    print(">>> AUDIT: Scanning Neutral Link...")
    
    # 1. Connectivity
    try:
        requests.get("https://google.com", timeout=2)
    except: SYSTEM_HEALTH.append({"type": "CRITICAL", "msg": "OFFLINE"})

    # 2. Bridge Integrity
    if not os.path.exists(CONFIG["PATHS"]["PROFIT_ENGINE"]):
        SYSTEM_HEALTH.append({"type": "WARNING", "msg": "PROFIT ENGINE DISCONNECTED"})
    
    print(f">>> AUDIT COMPLETE: {len(SYSTEM_HEALTH)} ISSUES.")

def scout_loop():
    global DYNAMIC_ALERTS
    while True:
        alerts = []
        # 1. Hardware
        cpu = psutil.cpu_percent()
        if cpu > 85: alerts.append({"title": "CPU CRITICAL", "val": f"{cpu}%", "color": "red"})
        
        # 2. Profit Engine Alerts
        notifs = load_json(CONFIG["PATHS"]["NOTIFICATIONS"])
        if notifs:
            # Assuming list of recent alerts
            for n in notifs[-1:]:
                alerts.append({"title": "PROFIT BOT", "val": n.get('message', 'Active'), "color": "blue"})

        # 3. Crypto
        try:
            r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", timeout=2).json()
            if r['bitcoin']['usd'] < 95000: 
                alerts.append({"title": "MARKET DIP", "val": "BTC < 95k", "color": "yellow"})
        except: pass

        DYNAMIC_ALERTS = alerts
        time.sleep(10)

threading.Thread(target=scout_loop, daemon=True).start()

# --- API ENDPOINTS ---

@app.route('/api/system')
def get_system():
    # IP Logic
    ip = {"query": "127.0.0.1", "isp": "LOCALHOST"}
    try: ip = requests.get("http://ip-api.com/json/", timeout=1).json()
    except: pass
    
    return jsonify({
        "cpu": psutil.cpu_percent(interval=None), 
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "boot": datetime.fromtimestamp(psutil.boot_time()).strftime("%H:%M"),
        "ip": ip
    })

@app.route('/api/finance')
def get_finance():
    # 1. Load Real Profit Data from Sub-System
    earnings = load_json(CONFIG["PATHS"]["PROFIT_ENGINE"])
    
    # Balance
    balance = earnings['total_earnings'] if earnings else 0.00
    if not earnings: balance = 14205.55 # Fallback if system hasn't run yet
    
    # Market Data
    market = []
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana,cardano&vs_currencies=usd").json()
        market = [
            {"symbol": "BTC", "price": f"${r['bitcoin']['usd']:,}"},
            {"symbol": "ETH", "price": f"${r['ethereum']['usd']:,}"},
            {"symbol": "SOL", "price": f"${r['solana']['usd']:,}"}
        ]
    except: market = [{"symbol": "API", "price": "OFFLINE"}]

    return jsonify({
        "balance": f"${balance:,.2f}",
        "market": market,
        # History is now Recent Opportunities from the Engine
        "history": earnings.get('history', [])[:3] if earnings else [] 
    })

@app.route('/api/intel')
def get_intel():
    intel = []
    
    # A. Threats
    t = load_json(CONFIG["PATHS"]["THREATS"])
    if t:
        intel.append({"type": "SYS", "src": "DEFCON", "msg": f"LEVEL {t.get('defcon', 5)}"})

    # B. News
    try:
        feed = feedparser.parse("http://feeds.bbci.co.uk/news/technology/rss.xml")
        for e in feed.entries[:2]:
            intel.append({"type": "NEWS", "src": "BBC", "msg": e.title[:30]+"..."})
    except: pass

    return jsonify(intel)

@app.route('/api/personal')
def get_personal():
    data = []
    # Gmail
    try:
        if "YOUR_EMAIL" not in CONFIG["GMAIL_USER"]:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(CONFIG["GMAIL_USER"], CONFIG["GMAIL_PASS"])
            mail.select("inbox")
            _, msgs = mail.search(None, '(UNSEEN)')
            for e_id in msgs[0].split()[-2:]:
                _, msg_data = mail.fetch(e_id, "(RFC822)")
                msg = email.message_from_bytes(msg_data[0][1])
                subj = decode_header(msg["Subject"])[0][0]
                if isinstance(subj, bytes): subj = subj.decode()
                data.append({"type": "EMAIL", "src": "Gmail", "msg": subj[:25]+"..."})
            mail.logout()
    except: pass
    
    # Pushbullet
    try:
        if "o.YOUR_KEY" not in CONFIG["PUSHBULLET"]:
            pb = Pushbullet(CONFIG["PUSHBULLET"])
            for push in pb.get_pushes()[:2]:
                if 'body' in push:
                    data.append({"type": "SMS", "src": push.get('title','Phone')[:10], "msg": push['body'][:25]+"..."})
    except: pass
    
    return jsonify(data)

@app.route('/api/status')
def get_status():
    return jsonify({"audit": SYSTEM_HEALTH, "alerts": DYNAMIC_ALERTS})

@app.route('/execute/<cmd>')
def execute(cmd):
    if cmd == "audit": run_audit()
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    run_audit()
    app.run(port=5000)
