from flask import Blueprint, request, jsonify
from core.storage.memory_vault import vault
from core.security.firewall import ZeroTrustFirewall
from core.ai.quant_agent import quant_engine
api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET'])
def status(): return jsonify({"status": "LONEWOLF ENTERPRISE GATEWAY ONLINE"}), 200

@api_bp.route('/oracle', methods=['POST', 'OPTIONS'])
def read_matrix():
    if request.method == "OPTIONS": return jsonify({"status": "ok"}), 200
    is_valid, err, code = ZeroTrustFirewall.verify_request(request.json, "FRONTEND_USER")
    if not is_valid: return err, code
    data = vault.get_matrix()
    if not data: return jsonify({"error": "AWAITING QUANT UPLINK"}), 503
    print("[ROUTER] 📡 Live Matrix Data successfully sent to Frontend!")
    return jsonify(data), 200

@api_bp.route('/update_oracle', methods=['POST'])
def write_matrix():
    is_valid, err, code = ZeroTrustFirewall.verify_request(request.json, "GITHUB_AI_CORE")
    if not is_valid: return err, code
    payload = request.json
    payload.pop("oracle_key", None)
    vault.update_matrix(payload)
    
    # Print the actual assets saved to RAM in the terminal!
    assets = list(payload.keys())
    print(f"[ROUTER] 💾 NEW DATA IMMUTABLY LOGGED IN RAM! Assets loaded: {assets}")
    return jsonify({"status": "MATRIX IMMUTABLY LOGGED"}), 200

@api_bp.route('/chat', methods=['POST', 'OPTIONS'])
def quant_chat():
    if request.method == "OPTIONS": return jsonify({"status": "ok"}), 200
    data = request.json
    if not data.get('message'): return jsonify({"error": "No query"}), 400
    
    print(f"[AI AGENT] 🧠 Processing query: {data['message'][:40]}...")
    reply = quant_engine.generate_risk_analysis(
        data['message'], data.get('zk_signature', 'UNVERIFIED'), 
        data.get('portfolio_state', 'No portfolio'), vault.get_matrix()
    )
    print("[AI AGENT] ✅ Reply Generated.")
    return jsonify({"reply": reply, "zk_signature": data.get('zk_signature')}), 200
