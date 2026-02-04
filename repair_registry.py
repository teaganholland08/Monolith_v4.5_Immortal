"""
DB REPAIR SCRIPT
Removes phantom agents from registry that no longer exist on disk.
"""
import sqlite3
from pathlib import Path

db_path = Path("System/Logs/ledger.db")
agents_dir = Path("System/Agents")

if not db_path.exists():
    print("No database found.")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all registered agents
cursor.execute("SELECT agent_name FROM agent_registry")
registered_agents = [row[0] for row in cursor.fetchall()]

print(f"Checking {len(registered_agents)} registered agents...")

for agent in registered_agents:
    script_path = agents_dir / f"{agent}.py"
    if not script_path.exists():
        print(f"❌ Phantom detected: {agent} (File not found)")
        cursor.execute("DELETE FROM agent_registry WHERE agent_name = ?", (agent,))
        print(f"   -> Removed from registry.")
    else:
        print(f"✅ Verified: {agent}")

conn.commit()
conn.close()
print("Registry repair complete.")
