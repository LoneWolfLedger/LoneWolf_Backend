from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai
import os
import json

app = Flask(__name__)
# Allow cross-origin requests securely
CORS(app, resources={r"/*": {"origins": "*"}})

# --- 1. SECURE VAULT EXTRACTION ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MASTER_KEY = os.environ.get("MASTER_KEY", "FALLBACK_KEY_UNSECURE") 

if GEMINI_API_KEY: genai.configure(api_key=GEMINI_API_KEY)
active_model = 'models/gemini-1.5-flash'
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
            active_model = m.name; break
except: pass
model = genai.GenerativeModel(active_model)

GLOBAL_MATRIX = {}

@app.route('/', methods=['GET'])
def system_status(): 
    return jsonify({"status": "ZERO-TRUST SECURE NODE ONLINE"}), 200

# --- 2. THE CRYPTOGRAPHIC LOCK (Read Data) ---
@app.route('/oracle', methods=['POST', 'OPTIONS'])
def get_oracle():
    if request.method == "OPTIONS": return jsonify({"status": "ok"}), 200
    
    data = request.json or {}
    # Server-side verification. The password is NEVER exposed to the frontend.
    if data.get("master_key") != MASTER_KEY:
        return jsonify({"error": "CRYPTOGRAPHIC VERIFICATION FAILED. ACCESS DENIED."}), 401
        
    if GLOBAL_MATRIX: return jsonify(GLOBAL_MATRIX)
    if os.path.exists("oracle_memory.json"):
        with open("oracle_memory.json", "r") as f: return jsonify(json.load(f))
    return jsonify({"error": "AWAITING HIGH-FREQUENCY UPLINK"}), 503

# --- 3. THE INJECTION FIREWALL (Write Data) ---
@app.route('/update_oracle', methods=['POST'])
def update_oracle():
    data = request.json
    if data.get("oracle_key") != MASTER_KEY: return jsonify({"error": "UNAUTHORIZED INJECTION"}), 401
    
    data.pop("oracle_key", None)
    global GLOBAL_MATRIX
    GLOBAL_MATRIX = data
    with open("oracle_memory.json", "w") as f: json.dump(GLOBAL_MATRIX, f)
    return jsonify({"status": "LIVE MATRIX SECURELY OVERWRITTEN"}), 200

@app.route('/chat', methods=['POST', 'OPTIONS'])
def oracle_chat():
    if request.method == "OPTIONS": return jsonify({"status": "ok"}), 200
    data = request.json
    user_message = data.get('message', '')
    zk_signature = data.get('zk_signature', 'UNVERIFIED')
    portfolio_state = data.get('portfolio_state', 'No portfolio connected.')
    
    if not user_message: return jsonify({"error": "No message"}), 400

    context = f"""
    You are CHRONOS-OMEGA, an elite Quantitative Portfolio Risk Manager. 
    User ZK-Signature: {zk_signature}. User Portfolio: {portfolio_state}
    Analyze their portfolio against current live market conditions. 
    Give exact, numerical, high-probability tips. Reply in a cold, elite, mathematical tone. Max 3 sentences. 
    User query: {user_message}
    """
    try:
        response = model.generate_content(context)
        return jsonify({"reply": response.text, "zk_signature": zk_signature})
    except Exception as e:
        return jsonify({"reply": f"COMM-LINK SEVERED. {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)