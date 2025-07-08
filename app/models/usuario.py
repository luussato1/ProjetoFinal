import hashlib

class Usuario:
    def __init__(self, id, username, password, email, nome_completo, is_admin=False):
        self.id = id
        self.username = username
        self.password = password  # Será armazenado como hash
        self.email = email
        self.nome_completo = nome_completo
        self.is_admin = is_admin

    def __repr__(self):
        return f"<Usuario {self.id}: {self.username}>"

    def to_dict(self):
        return self.__dict__
    
    @staticmethod
    def hash_password(password):
        """Gera hash da senha usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password):
        """Verifica se a senha fornecida corresponde ao hash armazenado"""
        return self.password == self.hash_password(password)

