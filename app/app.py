from flask import Flask
from routes.routes import routes

app = Flask(__name__, template_folder='views/html')

# Configuração da secret key para sessões
app.secret_key = 'petbus_secret_key_bmvc_2024'

from datetime import datetime

@app.context_processor
def inject_now():
    return {'now': datetime.now()}

app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
