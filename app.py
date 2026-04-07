from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai
import os
import json

app = Flask(__name__)
CORS(app) 

# --- ENTERPRISE AI ROUTING ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("[CRITICAL] GEMINI API KEY MISSING FROM RENDER ENVIRONMENT")

active_model = 'models/gemini-1.5-flash'
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
            active_model = m.name
            break
except Exception:
    pass

model = genai.GenerativeModel(active_model)

# --- GLOBAL MEMORY VAULT ---
GLOBAL_MATRIX = {}
MASTER_KEY = "021282" # The synchronized DevSecOps password

@app.route('/', methods=['GET', 'OPTIONS'])
def system_status():
    return jsonify({"status": "SINGULARITY ONLINE"}), 200

# FRONTEND CALLS THIS TO GET DATA
@app.route('/oracle', methods=['GET'])
def get_oracle():
    global GLOBAL_MATRIX
    if GLOBAL_MATRIX:
        return jsonify(GLOBAL_MATRIX)
    if os.path.exists("oracle_memory.json"):
        with open("oracle_memory.json", "r") as f:
            return jsonify(json.load(f))
    return jsonify({"error": "MATRIX COMPILING. AWAITING COLAB UPLINK."}), 503

# COLAB CALLS THIS TO INJECT DATA
@app.route('/update_oracle', methods=['POST'])
def update_oracle():
    data = request.json
    
    # 100% Firewall-Proof Password Check inside the JSON body
    if data.get("oracle_key") != MASTER_KEY:
        return jsonify({"error": "UNAUTHORIZED INJECTION"}), 401
    
    # Remove password before saving to public matrix
    data.pop("oracle_key", None)
    
    global GLOBAL_MATRIX
    GLOBAL_MATRIX = data
    
    with open("oracle_memory.json", "w") as f:
        json.dump(GLOBAL_MATRIX, f)
        
    return jsonify({"status": "MATRIX SUCCESSFULLY OVERWRITTEN"}), 200

@app.route('/chat', methods=['POST', 'OPTIONS'])
def oracle_chat():
    if request.method == "OPTIONS": return jsonify({"status": "ok"}), 200
    data = request.json
    user_message = data.get('message', '')
    zk_id = data.get('zk_id', 'UNKNOWN_ENTITY')
    
    if not user_message: return jsonify({"error": "No message"}), 400

    context = f"You are CHRONOS-OMEGA. User ZK-ID: {zk_id}. You use Kolmogorov-Arnold Networks to map markets. Reply in a cold, elite quantitative tone. Max 3 sentences. User query: {user_message}"
    
    try:
        response = model.generate_content(context)
        return jsonify({"reply": response.text, "zk_id": zk_id})
    except Exception as e:
        return jsonify({"reply": f"COMM-LINK SEVERED. DIAGNOSTIC: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)