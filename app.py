from flask import Flask
from flask_cors import CORS
from api.routes import api_bp
import threading, time, requests, os

RENDER_LIVE_URL = "https://lonewolf-backend.onrender.com/"

def autonomous_heartbeat():
    while True:
        time.sleep(840)
        try: requests.get(RENDER_LIVE_URL)
        except: pass

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.register_blueprint(api_bp)
    threading.Thread(target=autonomous_heartbeat, daemon=True).start()
    return app

app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, threaded=True)
