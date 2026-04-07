import os
from flask import jsonify

# Updated to your new key!
MASTER_KEY = os.environ.get("MASTER_KEY", "021282")

class ZeroTrustFirewall:
    @staticmethod
    def verify_request(data_payload, source="UNKNOWN"):
        print(f"\n[FIREWALL] 🛡️ Incoming connection from: {source}")
        
        if not data_payload: 
            print("[FIREWALL] ❌ REJECTED: Empty Payload")
            return False, jsonify({"error": "EMPTY PAYLOAD"}), 400
            
        key = data_payload.get("master_key") or data_payload.get("oracle_key")
        
        if key != MASTER_KEY: 
            print(f"[FIREWALL] ❌ REJECTED: Invalid Cryptographic Key used: '{key}'")
            return False, jsonify({"error": "DENIED"}), 401
            
        print("[FIREWALL] ✅ ACCESS GRANTED.")
        return True, None, 200
