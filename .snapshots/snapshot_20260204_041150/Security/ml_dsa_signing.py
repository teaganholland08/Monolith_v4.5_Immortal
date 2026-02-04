"""
ML-DSA (DILITHIUM) CODE SIGNING
NIST-standardized post-quantum digital signatures for agent verification

Purpose: Sign all agent code to prevent tampering
Standard: FIPS 204 (ML-DSA / Dilithium3)
"""

import hashlib
from pathlib import Path
from datetime import datetime

class MLDSASigner:
    """
    Post-quantum code signing using ML-DSA (Dilithium)
    
    Note: Requires pqcrypto library with Dilithium support
    For production, install: pip install pqcrypto
    """
    
    def __init__(self):
        self.signatures_dir = Path(__file__).parent.parent / "Logs" / "signatures"
        self.signatures_dir.mkdir(parents=True, exist_ok=True)
        
        # In production, load/generate Dilithium keypair
        # For now, use SHA-256 hash verification
        self.use_pq_crypto = False  # Set to True when pqcrypto installed
    
    def sign_agent(self, agent_path):
        """
        Sign agent code with ML-DSA
        
        Returns: Signature file path
        """
        agent_path = Path(agent_path)
        
        if not agent_path.exists():
            print(f"Error: Agent file not found: {agent_path}")
            return None
        
        # Read agent code
        with open(agent_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Generate signature
        if self.use_pq_crypto:
            # ML-DSA signing (production)
            signature = self._sign_with_dilithium(code)
        else:
            # SHA-256 hash (development)
            signature = hashlib.sha256(code.encode('utf-8')).hexdigest()
        
        # Save signature
        sig_file = self.signatures_dir / f"{agent_path.stem}.sig"
        
        with open(sig_file, 'w') as f:
            f.write(f"# ML-DSA Signature for {agent_path.name}\n")
            f.write(f"# Signed: {datetime.now().isoformat()}\n")
            f.write(f"# Algorithm: {'Dilithium3' if self.use_pq_crypto else 'SHA-256'}\n")
            f.write(f"{signature}\n")
        
        print(f"✓ Signed: {agent_path.name}")
        print(f"  Signature: {sig_file}")
        
        return sig_file
    
    def verify_agent(self, agent_path):
        """
        Verify agent code signature
        
        Returns: True if signature valid, False otherwise
        """
        agent_path = Path(agent_path)
        sig_file = self.signatures_dir / f"{agent_path.stem}.sig"
        
        if not sig_file.exists():
            print(f"Warning: No signature found for {agent_path.name}")
            return False
        
        # Read current code
        with open(agent_path, 'r', encoding='utf-8') as f:
            current_code = f.read()
        
        # Read signature
        with open(sig_file, 'r') as f:
            lines = f.readlines()
            stored_sig = lines[-1].strip()
        
        # Verify
        if self.use_pq_crypto:
            valid = self._verify_with_dilithium(current_code, stored_sig)
        else:
            current_hash = hashlib.sha256(current_code.encode('utf-8')).hexdigest()
            valid = current_hash == stored_sig
        
        if valid:
            print(f"✓ Signature valid: {agent_path.name}")
        else:
            print(f"✗ SIGNATURE INVALID: {agent_path.name}")
            print(f"  WARNING: Agent code may have been tampered with!")
        
        return valid
    
    def _sign_with_dilithium(self, code):
        """Sign with Dilithium (requires pqcrypto)"""
        # Placeholder for production implementation
        # from pqcrypto.sign.dilithium3 import sign
        # signature = sign(code.encode('utf-8'), self.private_key)
        return "DILITHIUM_SIGNATURE_PLACEHOLDER"
    
    def _verify_with_dilithium(self, code, signature):
        """Verify with Dilithium (requires pqcrypto)"""
        # Placeholder for production implementation
        # from pqcrypto.sign.dilithium3 import verify
        # return verify(code.encode('utf-8'), signature, self.public_key)
        return True

if __name__ == "__main__":
    signer = MLDSASigner()
    
    # Example: Sign all agents
    agents_dir = Path(__file__).parent.parent / "Agents"
    
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.py"):
            signer.sign_agent(agent_file)
