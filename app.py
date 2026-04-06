from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app) 

# !!! INJECT YOUR FREE GEMINI API KEY HERE !!!
GEMINI_API_KEY = "AIzaSyBN8L8lt23DIs_N5MxAOI_T9DGAsaY7QpA"
genai.configure(api_key=GEMINI_API_KEY)

# --- DYNAMIC FUTURE-PROOF MODEL SELECTION ---
# This automatically finds the newest active model so updates never break your app
active_model_name = 'models/gemini-1.5-flash'
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods and 'flash' in m.name:
            active_model_name = m.name
            break
except Exception as e:
    print(f"Model fetch error: {e}")

model = genai.GenerativeModel(active_model_name)

@app.route('/', methods=['GET', 'OPTIONS'])
def system_status():
    return jsonify({"status": "SINGULARITY ONLINE"}), 200

@app.route('/oracle', methods=['GET'])
def chronos_prediction():
    # Reads the Autonomous GitHub Matrix if it exists
    if os.path.exists("oracle_memory.json"):
        import json
        with open("oracle_memory.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    else:
        return jsonify({"error": "MATRIX COMPILING. AWAIT GITHUB CRON JOB."}), 503

@app.route('/chat', methods=['POST', 'OPTIONS'])
def oracle_chat():
    if request.method == "OPTIONS": # Bypasses CORS blocks
        return jsonify({"status": "ok"}), 200

    data = request.json
    user_message = data.get('message', '')
    zk_id = data.get('zk_id', 'UNKNOWN_ENTITY')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    system_context = f"""
    You are CHRONOS-OMEGA, an advanced quantitative AI. 
    The user's anonymous ZK-ID is {zk_id}. 
    You analyze financial markets using Liquid Differential Equations and Fourier Spectral Analysis.
    Respond in a cold, analytical, cyberpunk tone. Keep responses under 3 sentences.
    User message: {user_message}
    """
    
    try:
        response = model.generate_content(system_context)
        return jsonify({"reply": response.text, "zk_id": zk_id})
    except Exception as e:
        # DIAGNOSTIC FAILSAFE: Prints the exact Google error to the UI
        error_msg = str(e).replace('"', "'")
        return jsonify({"reply": f"COMM-LINK SEVERED. DIAGNOSTIC: {error_msg}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)