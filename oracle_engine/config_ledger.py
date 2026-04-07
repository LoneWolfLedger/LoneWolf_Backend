import hashlib, time, os
RENDER_API_URL = "https://lonewolf-backend.onrender.com/update_oracle"
MASTER_KEY = os.environ.get("MASTER_KEY", "021282")
TARGET_ACCURACY_BOUND = 0.85 

def generate_unique_user_hash(wallet_address, balance):
    nonce = str(time.time())
    payload = f"{wallet_address}-{balance}-{nonce}".encode()
    return "0x" + hashlib.sha384(payload).hexdigest()[:24]

def get_legal_disclaimer(confidence_score):
    return f"PROBABILITY SYNTHESIS: {confidence_score:.1f}%. LITERATURE MAPPING SECURED. NOT FINANCIAL ADVICE. RISK OF LOSS EXISTS (FAMA, 1970)."
