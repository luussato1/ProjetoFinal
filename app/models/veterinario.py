class Veterinario:
    def __init__(self, id, nome, crmv, especialidade, telefone, email):
        self.id = id
        self.nome = nome
        self.crmv = crmv
        self.especialidade = especialidade
        self.telefone = telefone
        self.email = email

    def __repr__(self):
        return f"<Veterinario {self.id}: {self.nome} ({self.crmv})>"

    def to_dict(self):
        return self.__dict__