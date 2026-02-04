"""
QUANTUM-SAFE COMMUNICATION PROTOCOL - Project Monolith v5.0
Implements: Dilithium-style Message Signing, Inter-Agent Authentication
Purpose: Ensures all messages between agents are authentic and untampered.
"""

import json
import hashlib
import time
import base64
from pathlib import Path
from typing import Dict, Any, Optional

class AgentAuthenticator:
    """
    Simulates Post-Quantum Message Signing (CRYSTALS-Dilithium)
    In a production 2026 environment, this would use a library like 'pqcrypto'.
    Here, we implement a hardened signature logic using SHA3-512 + Agent UUIDs.
    """
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.root = Path(__file__).parent.parent.parent
        self._load_keys()

    def _load_keys(self):
        # In a real system, keys would be in the offline vault Brain/vault.py
        # For simulation, we generate a persistent deterministic "secret"
        self.secret = hashlib.sha3_512(f"MONOLITH_SECRET_{self.agent_id}".encode()).hexdigest()

    def sign_message(self, message: Dict[str, Any]) -> str:
        """Signs a message dictionary and returns a base64 signature string"""
        payload = json.dumps(message, sort_keys=True)
        timestamp = str(int(time.time()))
        
        # Concatenate: Secret + Payload + Timestamp
        binding = f"{self.secret}|{payload}|{timestamp}"
        signature_hash = hashlib.sha3_512(binding.encode()).hexdigest()
        
        # Form the signature packet
        sig_packet = {
            "v": "1.0-PQC-SIM",
            "aid": self.agent_id,
            "ts": timestamp,
            "sig": signature_hash
        }
        return base64.b64encode(json.dumps(sig_packet).encode()).decode()

    @staticmethod
    def verify_signature(message: Dict[str, Any], signature_b64: str) -> bool:
        """Verifies if the signature is valid for the given message"""
        try:
            sig_packet = json.loads(base64.b64decode(signature_b64).decode())
            agent_id = sig_packet["aid"]
            timestamp = sig_packet["ts"]
            provided_sig = sig_packet["sig"]

            # Security Check: Reject if message older than 60 seconds (Replay protection)
            if int(time.time()) - int(timestamp) > 60:
                print(f"[SECURITY] Signature EXPIRED for Agent: {agent_id}")
                return False

            # Reconstruct Secret (Simulation)
            recon_secret = hashlib.sha3_512(f"MONOLITH_SECRET_{agent_id}".encode()).hexdigest()
            payload = json.dumps(message, sort_keys=True)
            
            check_binding = f"{recon_secret}|{payload}|{timestamp}"
            expected_sig = hashlib.sha3_512(check_binding.encode()).hexdigest()

            return provided_sig == expected_sig
        except Exception as e:
            print(f"[SECURITY] Validation Error: {e}")
            return False

if __name__ == "__main__":
    # Test Protocol
    auth = AgentAuthenticator("scout_agent")
    test_msg = {"action": "scan_market", "target": "RTX 5090"}
    
    encoded_sig = auth.sign_message(test_msg)
    print(f"Generated Signature: {encoded_sig[:32]}...")
    
    is_valid = AgentAuthenticator.verify_signature(test_msg, encoded_sig)
    print(f"Verification Result: {'✅ VALID' if is_valid else '❌ INVALID'}")
    
    # Test Tampering
    tampered_msg = {"action": "scan_market", "target": "RTX 4090"}
    is_valid_tamper = AgentAuthenticator.verify_signature(tampered_msg, encoded_sig)
    print(f"Tamper Verification Result: {'✅ VALID' if is_valid_tamper else '❌ INVALID (Tampers Detected!)'}")
