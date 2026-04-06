from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai
import time

app = Flask(__name__)
CORS(app) # Failsafe: Allows Vercel to connect

# !!! INJECT YOUR FREE GEMINI API KEY HERE !!!
GEMINI_API_KEY = "AIzaSyDClFXH0MjQr47W8SMXvhT2XwyRB3TBE3o"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/', methods=['GET', 'OPTIONS'])
def system_status():
    return jsonify({"status": "SINGULARITY ONLINE"}), 200

@app.route('/oracle', methods=['GET'])
def chronos_prediction():
    return jsonify({
        "asset": "^NSEI (NIFTY 50)",
        "current_price": "22450.00",
        "projected_target": "22610.45",
        "chronos_vector": "BULLISH BREAKOUT",
        "epistemic_uncertainty": "±42.50 INR",
        "spectral_resonance": "0.045 Hz",
        "accuracy_confidence": "89.4%"
    })

@app.route('/chat', methods=['POST'])
def oracle_chat():
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
        return jsonify({"reply": "COMM-LINK SEVERED. NEURAL OVERLOAD.", "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)