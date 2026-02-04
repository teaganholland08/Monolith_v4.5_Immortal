"""
GOVERNANCE & COMPLIANCE ENGINE - Best-in-World 2026 Enterprise Standard
Implements: Singapore MGF Framework, Continuous Monitoring, AI Audit Trail
Purpose: Enterprise-grade governance, regulatory compliance, and risk management.
"""

import json
import hashlib
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum
from dataclasses import dataclass, field, asdict


class RiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ComplianceStatus(Enum):
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    REQUIRES_REVIEW = "REQUIRES_REVIEW"


@dataclass
class ActionRecord:
    """Record of an AI agent action for audit trail"""
    agent_name: str
    action_type: str
    timestamp: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    human_approved: bool = False
    risk_level: str = "LOW"
    compliance_status: str = "COMPLIANT"
    metadata: Dict = field(default_factory=dict)


class GovernanceEngine:
    """
    AI Governance & Compliance Monitor
    Features:
    - Continuous compliance monitoring
    - Risk assessment per agent action
    - Human-in-the-loop (HITL) enforcement
    - Audit trail generation
    - Regulatory alignment (EU AI Act, Singapore MGF)
    """
    
    def __init__(self):
        self.root = Path(__file__).parent.parent.parent
        self.logs_dir = self.root / "System" / "Logs" / "Governance"
   
        self.audit_log = self.logs_dir / "audit_trail.jsonl"
        self.policy_file = self.root / "System" / "Config" / "governance_policy.json"
        
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        
        # Load governance policies
        self.policies = self._load_policies()
        
        # Track compliance metrics
        self.compliance_metrics = {
            "total_actions": 0,
            "compliant_actions": 0,
            "high_risk_actions": 0,
            "human_interventions": 0
        }
    
    def _load_policies(self) -> Dict:
        """Load governance policies from config"""
        if self.policy_file.exists():
            with open(self.policy_file, 'r') as f:
                return json.load(f)
        
        # Default policies aligned with Singapore MGF
        default_policies = {
            "high_risk_agents": ["investment_agent", "treasurer", "purchasing_agent"],
            "requires_human_approval": {
                "threshold_amount": 1000.0,  # Any transaction > $1000
                "critical_actions": ["execute_trade", "purchase_hardware", "transfer_funds"]
            },
            "data_retention": {
                "audit_logs_days": 2555,  # 7 years
                "action_records_days": 365
            },
            "risk_thresholds": {
                "LOW": {"max_transaction": 100},
                "MEDIUM": {"max_transaction": 1000},
                "HIGH": {"max_transaction": 10000},
                "CRITICAL": {"max_transaction": 999999}
            }
        }
        
        self.policy_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.policy_file, 'w') as f:
            json.dump(default_policies, f, indent=2)
        
        return default_policies
    
    def assess_risk(self, agent_name: str, action_type: str, inputs: Dict) -> RiskLevel:
        """Assess risk level of an AI action"""
        
        # Rule 1: High-risk agents
        if agent_name in self.policies.get("high_risk_agents", []):
            return RiskLevel.HIGH
        
        # Rule 2: Financial threshold
        amount = inputs.get("amount", 0)
        if amount > 10000:
            return RiskLevel.CRITICAL
        elif amount > 1000:
            return RiskLevel.HIGH
        elif amount > 100:
            return RiskLevel.MEDIUM
        
        # Rule 3: Critical actions
        if action_type in self.policies["requires_human_approval"]["critical_actions"]:
            return RiskLevel.HIGH
        
        return RiskLevel.LOW
    
    def requires_human_approval(self, risk_level: RiskLevel, action_type: str, inputs: Dict) -> bool:
        """Determine if action requires human approval"""
        
        # CRITICAL always requires approval
        if risk_level == RiskLevel.CRITICAL:
            return True
        
        # HIGH requires approval
        if risk_level == RiskLevel.HIGH:
            return True
        
        # Financial threshold check
        threshold = self.policies["requires_human_approval"].get("threshold_amount", 1000)
        if inputs.get("amount", 0) > threshold:
            return True
        
        # Critical action types
        if action_type in self.policies["requires_human_approval"]["critical_actions"]:
            return True
        
        return False
    
    def log_action(
        self,
        agent_name: str,
        action_type: str,
        inputs: Dict,
        outputs: Dict,
        human_approved: bool = False,
        metadata: Dict = None
    ) -> str:
        """Log an AI agent action for audit trail"""
        
        # Assess risk
        risk_level = self.assess_risk(agent_name, action_type, inputs)
        
        # Determine compliance
        compliance_status = ComplianceStatus.COMPLIANT
        if self.requires_human_approval(risk_level, action_type, inputs) and not human_approved:
            compliance_status = ComplianceStatus.REQUIRES_REVIEW
        
        # Create record
        record = ActionRecord(
            agent_name=agent_name,
            action_type=action_type,
            timestamp=datetime.now().isoformat(),
            inputs=inputs,
            outputs=outputs,
            human_approved=human_approved,
            risk_level=risk_level.value,
            compliance_status=compliance_status.value,
            metadata=metadata or {}
        )
        
        # Write to append-only audit log
        with open(self.audit_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(record)) + '\n')
        
        # Update metrics
        self.compliance_metrics["total_actions"] += 1
        if compliance_status == ComplianceStatus.COMPLIANT:
            self.compliance_metrics["compliant_actions"] += 1
        if risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
            self.compliance_metrics["high_risk_actions"] += 1
        if human_approved:
            self.compliance_metrics["human_interventions"] += 1
        
        # Generate unique action ID
        action_id = hashlib.sha256(
            f"{agent_name}{action_type}{record.timestamp}".encode()
        ).hexdigest()[:12]
        
        return action_id
    
    def get_compliance_report(self, days: int = 30) -> Dict:
        """Generate compliance report for last N days"""
        
        cutoff = datetime.now() - timedelta(days=days)
        records = []
        
        if self.audit_log.exists():
            with open(self.audit_log, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        record = json.loads(line.strip())
                        record_time = datetime.fromisoformat(record["timestamp"])
                        if record_time > cutoff:
                            records.append(record)
                    except:
                        pass
        
        # Analyze records
        total = len(records)
        compliant = sum(1 for r in records if r["compliance_status"] == "COMPLIANT")
        high_risk = sum(1 for r in records if r["risk_level"] in ["HIGH", "CRITICAL"])
        needs_review = sum(1 for r in records if r["compliance_status"] == "REQUIRES_REVIEW")
        
        return {
            "period_days": days,
            "total_actions": total,
            "compliant_actions": compliant,
            "compliance_rate": (compliant / max(1, total)) * 100,
            "high_risk_actions": high_risk,
            "requires_review": needs_review,
            "agent_breakdown": self._agent_breakdown(records),
            "generated_at": datetime.now().isoformat()
        }
    
    def _agent_breakdown(self, records: List[Dict]) -> Dict:
        """Break down actions by agent"""
        breakdown = {}
        for record in records:
            agent = record["agent_name"]
            if agent not in breakdown:
                breakdown[agent] = {"total": 0, "compliant": 0, "high_risk": 0}
            
            breakdown[agent]["total"] += 1
            if record["compliance_status"] == "COMPLIANT":
                breakdown[agent]["compliant"] += 1
            if record["risk_level"] in ["HIGH", "CRITICAL"]:
                breakdown[agent]["high_risk"] += 1
        
        return breakdown
    
    def check_data_retention(self):
        """Enforce data retention policies (e.g., 7-year audit logs)"""
        if not self.audit_log.exists():
            return {"removed": 0}
        
        # For audit logs, we keep everything (regulatory requirement)
        # But clean up old temp files
        retention_days = self.policies.get("data_retention", {}).get("audit_logs_days", 2555)
        cutoff = datetime.now() - timedelta(days=retention_days)
        
        # In a full implementation, we'd archive old logs to cold storage
        # For now, just report
        return {
            "retention_policy_days": retention_days,
            "cutoff_date": cutoff.isoformat(),
            "status": "audit_logs_preserved"
        }


# Singleton
_governance = None

def get_governance() -> GovernanceEngine:
    """Get the global governance engine"""
    global _governance
    if _governance is None:
        _governance = GovernanceEngine()
    return _governance


if __name__ == "__main__":
    # Demo
    gov = get_governance()
    
    # Log some test actions
    gov.log_action(
        "investment_agent",
        "execute_trade",
        {"symbol": "BTC", "amount": 5000},
        {"status": "pending_approval"},
        human_approved=False
    )
    
    gov.log_action(
        "backup_agent",
        "create_snapshot",
        {},
        {"snapshot_id": "snap_123", "files": 22},
        human_approved=False
    )
    
    # Generate report
    report = gov.get_compliance_report(days=30)
    print(f"Compliance Report: {json.dumps(report, indent=2)}")
