import os
from flask import jsonify
MASTER_KEY = os.environ.get("MASTER_KEY", "OMEGA-777")
class ZeroTrustFirewall:
    @staticmethod
    def verify_request(data_payload):
        if not data_payload: return False, jsonify({"error": "EMPTY PAYLOAD"}), 400
        key = data_payload.get("master_key") or data_payload.get("oracle_key")
        if key != MASTER_KEY: return False, jsonify({"error": "DENIED"}), 401
        return True, None, 200
