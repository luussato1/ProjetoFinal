class Cliente:
    def __init__(self, id, nome, email, telefone, endereco):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

    def __repr__(self):
        return f"<Cliente {self.id}: {self.nome}>"

    def to_dict(self):
        return self.__dict__
        
