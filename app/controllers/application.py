from models.database import Database
from models.cliente import Cliente
from models.animal import Animal
from models.veterinario import Veterinario
from models.consulta import Consulta

class ClienteController:
    @staticmethod
    def listar():
        db = Database.load()
        return db["clientes"]

    @staticmethod
    def adicionar(cliente):
        db = Database.load()
        db["clientes"].append(cliente.to_dict())
        Database.save(db)

    @staticmethod
    def remover(cliente_id):
        db = Database.load()
        db["clientes"] = [c for c in db["clientes"] if c["id"] != cliente_id]
        Database.save(db)

    @staticmethod
    def atualizar(cliente_atualizado):
        db = Database.load()
        for i, c in enumerate(db["clientes"]):
            if c["id"] == cliente_atualizado.id:
                db["clientes"][i] = cliente_atualizado.to_dict()
                break
        Database.save(db)

class AnimalController:
    @staticmethod
    def listar():
        db = Database.load()
        return db["animais"]

    @staticmethod
    def adicionar(animal):
        db = Database.load()
        db["animais"].append(animal.to_dict())
        Database.save(db)

    @staticmethod
    def remover(animal_id):
        db = Database.load()
        db["animais"] = [a for a in db["animais"] if a["id"] != animal_id]
        Database.save(db)

    @staticmethod
    def atualizar(animal_atualizado):
        db = Database.load()
        for i, a in enumerate(db["animais"]):
            if a["id"] == animal_atualizado.id:
                db["animais"][i] = animal_atualizado.to_dict()
                break
        Database.save(db)

class VeterinarioController:
    @staticmethod
    def listar():
        db = Database.load()
        return db["veterinarios"]

    @staticmethod
    def adicionar(veterinario):
        db = Database.load()
        db["veterinarios"].append(veterinario.to_dict())
        Database.save(db)

    @staticmethod
    def remover(veterinario_id):
        db = Database.load()
        db["veterinarios"] = [v for v in db["veterinarios"] if v["id"] != veterinario_id]
        Database.save(db)

    @staticmethod
    def atualizar(veterinario_atualizado):
        db = Database.load()
        for i, v in enumerate(db["veterinarios"]):
            if v["id"] == veterinario_atualizado.id:
                db["veterinarios"][i] = veterinario_atualizado.to_dict()
                break
        Database.save(db)

class ConsultaController:
    @staticmethod
    def listar():
        db = Database.load()
        return db["consultas"]

    @staticmethod
    def adicionar(consulta):
        db = Database.load()
        db["consultas"].append(consulta.to_dict())
        Database.save(db)

    @staticmethod
    def remover(consulta_id):
        db = Database.load()
        db["consultas"] = [c for c in db["consultas"] if c["id"] != consulta_id]
        Database.save(db)

    @staticmethod
    def atualizar(consulta_atualizada):
        db = Database.load()
        for i, c in enumerate(db["consultas"]):
            if c["id"] == consulta_atualizada.id:
                db["consultas"][i] = consulta_atualizada.to_dict()
                break
        Database.save(db)        