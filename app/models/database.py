import json
import os

DB_FILE = os.path.join(os.path.dirname(__file__), '../../data/db.json')

class Database:
    @staticmethod
    def load():
        if not os.path.exists(DB_FILE):
            os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)  # Garante que a pasta data/ existe
            with open(DB_FILE, 'w') as f:
                json.dump({
                    "clientes": [],
                    "animais": [],
                    "veterinarios": [],
                    "consultas": []
                }, f)

        with open(DB_FILE, 'r') as f:
            return json.load(f)

    @staticmethod
    def save(data):
        with open(DB_FILE, 'w') as f:
            json.dump(data, f, indent=4)
