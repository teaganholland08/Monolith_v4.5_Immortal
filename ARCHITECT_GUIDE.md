# THE ARCHITECT - BUILD ANY AGENT YOU NEED

**Purpose:** Create new agents on-demand without coding  
**Pattern:** Recursive Agentic Architecture  
**Philosophy:** Tell it WHAT, it builds HOW

---

## HOW IT WORKS

### The Factory Pattern

```
User Need → Meta-Orchestrator → Architect → New Agent → Registry
```

1. You identify a need ("Track off-grid land prices")
2. Monolith Prime realizes no agent exists
3. The Architect writes Python code for the new agent
4. Agent is registered and activated
5. Agent runs autonomously, creates .done sentinel
6. You review results in 15-minute briefing

---

## BUILDING YOUR FIRST CUSTOM AGENT

### Example: Real Estate Scout

```python
from monolith_prime import MonolithPrime

prime = MonolithPrime()

# Define what the agent should do
scout_code = '''"""
Real Estate Scout - Kootenays Region
Tracks off-grid land prices in BC
"""
import json
from pathlib import Path
from datetime import datetime

# In production: scrape realtor.ca or API
land_listings = [
    {"location": "Nelson, BC", "acres": 40, "price": 150000},
    {"location": "Kaslo, BC", "acres": 80, "price": 280000}
]

# Create sentinel for Director review
sentinel_dir = Path(__file__).parent.parent / "Sentinels"
sentinel_dir.mkdir(exist_ok=True)

sentinel_data = {
    "agent": "scout_kootenays",
    "message": f"Found {len(land_listings)} land opportunities",
    "data": land_listings,
    "timestamp": datetime.now().isoformat()
}

with open(sentinel_dir / "scout_kootenays.done", 'w') as f:
    json.dump(sentinel_data, f, indent=2)

print(f"✅ Scout: {len(land_listings)} listings found")
'''

# Build the agent
prime.architect_build_agent(
    agent_name="scout_kootenays",
    purpose="Track off-grid land prices in Kootenays",
    code_template=scout_code
)

# Run it
prime.run_agent("scout_kootenays")
```

---

## AGENT TEMPLATES

### Revenue Scanner

```python
revenue_scanner = '''
import requests
from datetime import datetime

# Check Gumroad sales
response = requests.get(
    "https://api.gumroad.com/v2/sales",
    headers={"Authorization": f"Bearer {GUMROAD_TOKEN}"}
)

sales_today = len(response.json()["sales"])

# Create sentinel
# ... (standard sentinel pattern)
'''
```

### Tax Loophole Hunter

```python
loophole_hunter = '''
import requests
from bs4 import BeautifulSoup

# Scrape Canada Revenue Agency updates
cra_url = "https://www.canada.ca/en/revenue-agency/news.html"
response = requests.get(cra_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Look for keywords: "credit", "deduction", "exemption"
loopholes_found = []
# ... (parsing logic)

# Create sentinel with findings
'''
```

### Smart Home Monitor

```python
home_monitor = '''
import requests

# Check Home Assistant status
ha_url = "http://homeassistant.local:8123/api"
headers = {"Authorization": f"Bearer {HA_TOKEN}"}

entities = requests.get(f"{ha_url}/states", headers=headers).json()

# Check for anomalies (doors unlocked, high power usage, etc.)
# ... (analysis logic)

# Create sentinel if issues found
'''
```

---

## THE SENTINEL PATTERN

### What is a Sentinel?

A `.done` file that signals completion for your 15-minute review.

### Format

```json
{
  "agent": "agent_name",
  "message": "Human-readable summary",
  "data": { ... },
  "timestamp": "2026-02-03T22:40:00Z"
}
```

### Why It Works

- **No Noise:** Only completed tasks appear
- **Fast Review:** Open file, read summary, decide
- **One-Click Clear:** Delete .done file after review

---

## AGENT LIFECYCLE

### 1. Creation

```python
prime.architect_build_agent(name, purpose, code)
```

- Writes Python file to `System/Agents/`
- Adds to Agent Registry database
- Status: ACTIVE

### 2. Execution

```python
prime.run_agent(name)
```

- Runs in subprocess (sandboxed)
- 30-second timeout
- Captures output/errors

### 3. Completion

```python
# Agent creates sentinel
sentinel_data = {...}
with open(f"{name}.done", 'w') as f:
    json.dump(sentinel_data, f)
```

### 4. Review (15-Minute Briefing)

```python
updates = prime.check_sentinels()
for update in updates:
    print(update["message"])
    # Decide: approve, reject, modify
```

### 5. Cleanup

```python
prime.clear_sentinel("agent_name.done")
```

---

## GOD RULES FOR AGENTS

### Rule 1: 2026 Best Practices

Every agent MUST use the latest libraries:

- ✅ `requests` (HTTP)
- ✅ `beautifulsoup4` (scraping)
- ✅ `sqlite3` (database)
- ❌ Legacy methods (urllib, manual HTML parsing)

### Rule 2: Sandboxed Execution

- All agents run in subprocess
- 30-second timeout
- Cannot access parent process memory

### Rule 3: Sentinel Required

- Every agent MUST create a .done file
- Director only sees what's complete
- No logs, no noise

### Rule 4: Earnings Tracked

- If agent generates revenue, log it
- Registry tracks earnings_generated
- Auto-prioritizes profitable agents

---

## ADVANCED: AGENT EVOLUTION

### Self-Improving Agents

```python
# Agent can request its own upgrade
upgrade_request = {
    "agent": "revenue_monitor",
    "request": "Add crypto trading monitoring",
    "priority": "HIGH"
}

# Meta-Orchestrator sees request
# Architect rewrites agent with new capability
# Old agent archived, new agent activated
```

### Multi-Agent Collaboration

```python
# Scout finds land
scout_kootenays.run()

# Analyst calculates ROI
analyst_roi.run(scout_kootenays.results)

# Treasurer decides to purchase
treasurer.approve_purchase(analyst_roi.recommendation)
```

---

## REGISTRY COMMANDS

### List All Agents

```python
prime.list_agents()
```

### Deactivate Agent

```python
conn = sqlite3.connect(prime.db_path)
cursor = conn.cursor()
cursor.execute("UPDATE agent_registry SET status = 'INACTIVE' WHERE agent_name = ?", ("agent_name",))
conn.commit()
```

### Check Agent Earnings

```python
cursor.execute("SELECT earnings_generated FROM agent_registry WHERE agent_name = ?", ("revenue_monitor",))
earnings = cursor.fetchone()[0]
```

---

## YOUR 15-MINUTE WORKFLOW

### Morning (7:00 AM)

1. Run `python monolith_prime.py`
2. Check sentinels (updates waiting)
3. Review each .done file:
   - Revenue: Note amount
   - Loopholes: Decide to pursue
   - Land: Save listing or reject
4. Clear sentinels
5. (Optional) Give new directive: "Build agent to track X"

### Rest of Day

- Agents run autonomously
- Create .done files when complete
- No interruptions

---

**STATUS:** Recursive Agent Factory - OPERATIONAL  
**AGENTS:** Build unlimited, specialized workers  
**USER TIME:** 15 minutes/day maximum
