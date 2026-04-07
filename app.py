from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai
import os
import json

app = Flask(__name__)
CORS(app) 

# --- GEMINI AI SETUP ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("[CRITICAL ERROR] GEMINI API KEY MISSING")

active_model_name = 'models/gemini-1.5-flash'
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
            active_model_name = m.name
            break
except Exception:
    pass

model = genai.GenerativeModel(active_model_name)

# --- GLOBAL MEMORY STORAGE ---
# Render will hold the data in this variable
GLOBAL_MATRIX = {}
ORACLE_PASSWORD = "OMEGA-777" # The key Colab must use to inject data

@app.route('/', methods=['GET', 'OPTIONS'])
def system_status():
    return jsonify({"status": "SINGULARITY ONLINE"}), 200

# 1. FRONTEND CALLS THIS TO READ THE DATA
@app.route('/oracle', methods=['GET'])
def chronos_prediction():
    if GLOBAL_MATRIX:
        return jsonify(GLOBAL_MATRIX)
    
    # Failsafe: Try reading local file if RAM was wiped during sleep
    if os.path.exists("oracle_memory.json"):
        with open("oracle_memory.json", "r") as f:
            return jsonify(json.load(f))
            
    return jsonify({"error": "MATRIX COMPILING. AWAITING COLAB UPLINK."}), 503

# 2. COLAB CALLS THIS TO INJECT NEW DATA
# 2. COLAB CALLS THIS TO INJECT NEW DATA
@app.route('/update_oracle', methods=['POST'])
def update_oracle():
    data = request.json
    
    # Check the password INSIDE the payload instead of the headers
    if data.get("oracle_key") != "OMEGA-777":
        return jsonify({"error": "UNAUTHORIZED INJECTION"}), 401
    
    # Remove the password before saving to the public matrix
    data.pop("oracle_key", None)
    
    global GLOBAL_MATRIX
    GLOBAL_MATRIX = data
    
    # Save to disk so it survives server restarts
    with open("oracle_memory.json", "w") as f:
        import json
        json.dump(GLOBAL_MATRIX, f)
        
    return jsonify({"status": "MATRIX SUCCESSFULLY OVERWRITTEN"}), 200

@app.route('/chat', methods=['POST', 'OPTIONS'])
def oracle_chat():
    if request.method == "OPTIONS": return jsonify({"status": "ok"}), 200
    data = request.json
    user_message = data.get('message', '')
    zk_id = data.get('zk_id', 'UNKNOWN_ENTITY')
    
    if not user_message: return jsonify({"error": "No message"}), 400

    system_context = f"You are CHRONOS-OMEGA. User ZK-ID: {zk_id}. You use Kolmogorov-Arnold Networks and Hurst Exponents to map market chaos. Reply in a cold, elite quantitative tone. Max 3 sentences. User: {user_message}"
    
    try:
        response = model.generate_content(system_context)
        return jsonify({"reply": response.text, "zk_id": zk_id})
    except Exception as e:
        return jsonify({"reply": f"COMM-LINK SEVERED. DIAGNOSTIC: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)