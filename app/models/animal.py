class Animal:
    def __init__(self, id, nome, especie,  id_cliente, raca, idade=0, peso=0.0):
        self.id = id
        self.nome = nome
        self.especie = especie
        self.id_cliente = id_cliente
        self.raca = raca
        self.idade = idade
        self.peso = peso

    def __repr__(self):
        return f"<Animal {self.id}: {self.nome} ({self.especie})>"

    def to_dict(self):
        return self.__dict__


