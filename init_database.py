"""
MONOLITH DATABASE INITIALIZATION
Creates all required tables for autonomous operation

Tables:
- transactions: Revenue, expenses, trades
- tasks: Event-driven task queue
- approvals: Pending Director decisions
- god_rules_log: Audit trail of rule enforcement
"""

import sqlite3
from pathlib import Path
from datetime import datetime

def init_database():
    """Initialize all Monolith tables"""
    
    db_path = Path(__file__).parent / "System" / "Logs" / "ledger.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            type TEXT NOT NULL,
            action TEXT,
            amount REAL NOT NULL,
            asset TEXT,
            timestamp TEXT NOT NULL,
            notes TEXT
        )
    """)
    
    # Task queue
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_type TEXT NOT NULL,
            priority INTEGER DEFAULT 5,
            data TEXT,
            status TEXT DEFAULT 'PENDING',
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
    """)
    
    # Approval queue
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            cost REAL NOT NULL,
            category TEXT,
            justification TEXT,
            status TEXT DEFAULT 'PENDING',
            created_at TEXT NOT NULL,
            approved_at TEXT
        )
    """)
    
    # God Rules audit log
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS god_rules_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT NOT NULL,
            action TEXT NOT NULL,
            result TEXT NOT NULL,
            details TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    
    # System events
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            source TEXT NOT NULL,
            data TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized: {db_path}")
    print("   Tables created:")
    print("   • transactions (revenue/expense tracking)")
    print("   • tasks (event-driven queue)")
    print("   • approvals (Director decisions)")
    print("   • god_rules_log (safety audit trail)")
    print("   • events (system activity)")

if __name__ == "__main__":
    init_database()
