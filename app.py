from flask import Flask
from flask_cors import CORS
from api.routes import api_bp
import threading
import time
import requests
import os

# --- DEVOPS VARIABLES ---
# Change this to your exact Render URL if it is different
RENDER_LIVE_URL = "https://lonewolf-backend.onrender.com/"

def autonomous_heartbeat():
    """
    THE IMMORTALITY HACK: 
    A background Daemon Thread that recursively pings its own server 
    every 14 minutes to mathematically bypass Render's 15-minute sleep protocol.
    """
    while True:
        time.sleep(840)  # 840 seconds = 14 minutes
        try:
            # The server reaches out to the internet and hits its own endpoint
            response = requests.get(RENDER_LIVE_URL)
            if response.status_code == 200:
                print("[HEARTBEAT] Recursive Ping Successful. Sleep Protocol Bypassed.")
        except Exception as e:
            print(f"[HEARTBEAT] Fault Detected: {e}")

def create_app():
    """Enterprise App Factory Pattern with Heartbeat Ignition."""
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Register the highly scalable Blueprint architecture
    app.register_blueprint(api_bp)
    
    # IGNITE THE IMMORTALITY THREAD (Runs silently in the background)
    heartbeat_thread = threading.Thread(target=autonomous_heartbeat, daemon=True)
    heartbeat_thread.start()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, threaded=True)