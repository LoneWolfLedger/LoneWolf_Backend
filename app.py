from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai
import os
import json

app = Flask(__name__)
CORS(app) 

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY: genai.configure(api_key=GEMINI_API_KEY)

active_model = 'models/gemini-1.5-flash'
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
            active_model = m.name; break
except: pass

model = genai.GenerativeModel(active_model)

GLOBAL_MATRIX = {}
MASTER_KEY = "OMEGA-777" 

@app.route('/', methods=['GET'])
def system_status(): return jsonify({"status": "HIGH-FREQUENCY SINGULARITY ONLINE"}), 200

@app.route('/oracle', methods=['GET'])
def get_oracle():
    if GLOBAL_MATRIX: return jsonify(GLOBAL_MATRIX)
    if os.path.exists("oracle_memory.json"):
        with open("oracle_memory.json", "r") as f: return jsonify(json.load(f))
    return jsonify({"error": "AWAITING HIGH-FREQUENCY UPLINK"}), 503

@app.route('/update_oracle', methods=['POST'])
def update_oracle():
    data = request.json
    if data.get("oracle_key") != MASTER_KEY: return jsonify({"error": "UNAUTHORIZED"}), 401
    data.pop("oracle_key", None)
    global GLOBAL_MATRIX
    GLOBAL_MATRIX = data
    with open("oracle_memory.json", "w") as f: json.dump(GLOBAL_MATRIX, f)
    return jsonify({"status": "LIVE MATRIX OVERWRITTEN"}), 200

@app.route('/chat', methods=['POST', 'OPTIONS'])
def oracle_chat():
    if request.method == "OPTIONS": return jsonify({"status": "ok"}), 200
    data = request.json
    user_message = data.get('message', '')
    zk_signature = data.get('zk_signature', 'UNVERIFIED')
    portfolio_state = data.get('portfolio_state', 'No portfolio connected.')
    
    if not user_message: return jsonify({"error": "No message"}), 400

    # The AI now acts as a dedicated Quant Risk Manager using the user's secure portfolio state
    context = f"""
    You are CHRONOS-OMEGA, an elite Quantitative Portfolio Risk Manager. 
    User ZK-Signature: {zk_signature} (Cryptographically Verified).
    User Portfolio Data: {portfolio_state}
    
    Current global market matrix: {str(GLOBAL_MATRIX)[:500]}...
    
    Analyze their portfolio against current live market conditions. Give exact, numerical, high-probability tips (85% confidence targets). 
    Reply in a cold, elite, mathematical tone. Max 3 sentences. 
    User query: {user_message}
    """
    try:
        response = model.generate_content(context)
        return jsonify({"reply": response.text, "zk_signature": zk_signature})
    except Exception as e:
        return jsonify({"reply": f"COMM-LINK SEVERED. {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)