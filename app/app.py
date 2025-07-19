from flask import Flask
from websocket_manager import socketio, init_socketio

app = Flask(__name__, template_folder="views/html")

app.secret_key = "petbus_secret_key_bmvc_2024"

init_socketio(app)

from datetime import datetime

@app.context_processor
def inject_now():
    return {"now": datetime.now()}

from routes.routes import routes
app.register_blueprint(routes)

import controllers.websocket_events

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)


