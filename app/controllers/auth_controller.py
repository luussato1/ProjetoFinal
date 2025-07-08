from models.database import Database
from models.usuario import Usuario
from flask import session

class AuthController:
    @staticmethod
    def listar_usuarios():
        db = Database.load()
        return db.get("usuarios", [])

    @staticmethod
    def adicionar_usuario(usuario):
        db = Database.load()
        if "usuarios" not in db:
            db["usuarios"] = []
        db["usuarios"].append(usuario.to_dict())
        Database.save(db)

    @staticmethod
    def buscar_por_username(username):
        usuarios = AuthController.listar_usuarios()
        for usuario_data in usuarios:
            if usuario_data["username"] == username:
                return Usuario(**usuario_data)
        return None

    @staticmethod
    def autenticar(username, password):
        usuario = AuthController.buscar_por_username(username)
        if usuario and usuario.check_password(password):
            return usuario
        return None

    @staticmethod
    def fazer_login(usuario):
        session['user_id'] = usuario.id
        session['username'] = usuario.username
        session['is_admin'] = usuario.is_admin
        session['logged_in'] = True

    @staticmethod
    def fazer_logout():
        session.clear()

    @staticmethod
    def usuario_logado():
        return session.get('logged_in', False)

    @staticmethod
    def usuario_atual():
        if AuthController.usuario_logado():
            return {
                'id': session.get('user_id'),
                'username': session.get('username'),
                'is_admin': session.get('is_admin', False)
            }
        return None

    @staticmethod
    def is_admin():
        return session.get('is_admin', False)

