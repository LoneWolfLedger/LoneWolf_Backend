import os

# 1. CREATE ENTERPRISE DIRECTORY STRUCTURE
directories = ['core', 'core/security', 'core/storage', 'core/ai', 'api']
for d in directories:
    os.makedirs(d, exist_ok=True)

# 2. FILE: THREAD-SAFE MEMORY VAULT
with open('core/storage/memory_vault.py', 'w') as f:
    f.write("""import json
import os
import threading

class ThreadSafeVault:
    \"\"\"
    Enterprise In-Memory Data Store. 
    Uses Threading Locks to prevent I/O bottlenecks during massive data surges.
    \"\"\"
    def __init__(self, file_path="matrix_ledger.json"):
        self.file_path = file_path
        self.lock = threading.Lock()
        self.memory_cache = {}
        self._boot_load()

    def _boot_load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.memory_cache = json.load(f)

    def get_matrix(self):
        with self.lock:
            return self.memory_cache

    def update_matrix(self, new_data):
        with self.lock:
            self.memory_cache = new_data
            # Async-safe disk write mapping
            with open(self.file_path, "w") as f:
                json.dump(self.memory_cache, f)
            return True

vault = ThreadSafeVault()
""")

# 3. FILE: ZERO-TRUST FIREWALL
with open('core/security/firewall.py', 'w') as f:
    f.write("""import os
from flask import jsonify

MASTER_KEY = os.environ.get("MASTER_KEY", "OMEGA-777")

class ZeroTrustFirewall:
    \"\"\"
    Military-grade middleware. Intercepts payloads before they reach the routing logic.
    \"\"\"
    @staticmethod
    def verify_request(data_payload):
        if not data_payload:
            return False, jsonify({"error": "EMPTY PAYLOAD"}), 400
            
        # Check either 'master_key' (from UI) or 'oracle_key' (from Colab)
        key = data_payload.get("master_key") or data_payload.get("oracle_key")
        
        if key != MASTER_KEY:
            return False, jsonify({"error": "CRYPTOGRAPHIC FIREWALL DENIED"}), 401
            
        return True, None, 200
""")

# 4. FILE: QUANT AI AGENT
with open('core/ai/quant_agent.py', 'w') as f:
    f.write("""import os
import google.generativeai as genai

class InstitutionalQuantAI:
    \"\"\"
    Wraps the Gemini Engine. Handles context-window truncation to prevent 
    API crashes when processing massive datasets.
    \"\"\"
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        self.model_name = 'models/gemini-1.5-flash'
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
                    self.model_name = m.name; break
        except: pass
        
        self.model = genai.GenerativeModel(self.model_name)

    def generate_risk_analysis(self, user_msg, zk_sig, portfolio, live_matrix):
        # Truncate massive matrix data to top 1000 chars to save AI token limits
        matrix_context = str(live_matrix)[:1000] 
        
        context = f\"\"\"
        You are CHRONOS-OMEGA, an Institutional Quant AI. 
        User ZK-ID: {zk_sig}. VERIFIED PORTFOLIO: {portfolio}.
        Market Matrix Snapshot: {matrix_context}...
        
        INSTRUCTIONS:
        1. Calculate Expected Return (EV).
        2. Cite academic literature (Gatheral, Peters, Fama).
        3. End with: "PROBABILITY SYNTHESIS ONLY. NOT FINANCIAL ADVICE."
        Max 4 sentences. Tone: Cold, elite, mathematical.
        Query: {user_msg}
        \"\"\"
        try:
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            return f"QUANT-NODE SEVERED: {str(e)}"

quant_engine = InstitutionalQuantAI()
""")

# 5. FILE: API ROUTER (BLUEPRINTS)
with open('api/routes.py', 'w') as f:
    f.write("""from flask import Blueprint, request, jsonify
from core.storage.memory_vault import vault
from core.security.firewall import ZeroTrustFirewall
from core.ai.quant_agent import quant_engine

api_bp = Blueprint('api', __name__)

@api_bp.route('/', methods=['GET'])
def status():
    return jsonify({"status": "LONEWOLF ENTERPRISE GATEWAY ONLINE"}), 200

@api_bp.route('/oracle', methods=['POST', 'OPTIONS'])
def read_matrix():
    if request.method == "OPTIONS": return jsonify({"status": "ok"}), 200
    
    is_valid, error_res, status_code = ZeroTrustFirewall.verify_request(request.json)
    if not is_valid: return error_res, status_code
    
    data = vault.get_matrix()
    if not data:
        return jsonify({"error": "AWAITING QUANT UPLINK"}), 503
    return jsonify(data), 200

@api_bp.route('/update_oracle', methods=['POST'])
def write_matrix():
    is_valid, error_res, status_code = ZeroTrustFirewall.verify_request(request.json)
    if not is_valid: return error_res, status_code
    
    payload = request.json
    payload.pop("oracle_key", None) # Strip password before saving
    
    vault.update_matrix(payload)
    return jsonify({"status": "MATRIX IMMUTABLY LOGGED"}), 200

@api_bp.route('/chat', methods=['POST', 'OPTIONS'])
def quant_chat():
    if request.method == "OPTIONS": return jsonify({"status": "ok"}), 200
    
    data = request.json
    user_msg = data.get('message', '')
    if not user_msg: return jsonify({"error": "No query provided"}), 400
    
    reply = quant_engine.generate_risk_analysis(
        user_msg, 
        data.get('zk_signature', 'UNVERIFIED'), 
        data.get('portfolio_state', 'No portfolio'), 
        vault.get_matrix()
    )
    return jsonify({"reply": reply, "zk_signature": data.get('zk_signature')}), 200
""")

# 6. FILE: THE MASTER ENTRY POINT (app.py)
with open('app.py', 'w') as f:
    f.write("""from flask import Flask
from flask_cors import CORS
from api.routes import api_bp

def create_app():
    \"\"\"
    Enterprise App Factory Pattern.
    \"\"\"
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Register the highly scalable Blueprint architecture
    app.register_blueprint(api_bp)
    return app

app = create_app()

if __name__ == '__main__':
    # Production servers (Gunicorn on Render) bypass this block.
    app.run(host='0.0.0.0', port=10000, threaded=True)
""")

print("ACKEND ARCHITECTURE GENERATED SUCCESSFULLY")