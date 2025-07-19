from datetime import datetime

class Consulta:
    def __init__(self, id, id_animal, id_veterinario, data_consulta, 
                 motivo, diagnostico, tratamento, observacoes, valor=0.0):
        self.id = id
        self.id_animal = id_animal
        self.id_veterinario = id_veterinario
        self.data_consulta = data_consulta or datetime.now()
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.tratamento = tratamento
        self.observacoes = observacoes
        self.valor = valor

    def __repr__(self):
        return f"<Consulta {self.id}: Animal {self.id_animal} - {self.data_consulta}>"

    def to_dict(self):
        data = self.__dict__.copy()
        if isinstance(data['data_consulta'], datetime):
            data['data_consulta'] = data['data_consulta'].isoformat()
        return data
