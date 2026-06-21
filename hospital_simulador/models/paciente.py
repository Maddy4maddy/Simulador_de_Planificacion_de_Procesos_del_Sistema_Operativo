class Paciente:
    TIPOS_PRIORIDAD = {
        "Rojo": 5,
        "Amarillo": 4,
        "Embarazada": 3,
        "Verde": 2,
        "Cita": 1,
        "Seguimiento": 0
    }
    
    def __init__(self, id_paciente, nombre, tipo, tiempo_llegada, rafaga, prioridad=None, gestiones=1):
        self.id = id_paciente
        self.nombre = nombre
        self.tipo = tipo
        self.tiempo_llegada = tiempo_llegada
        self.rafaga = rafaga
        self.prioridad = prioridad if prioridad is not None else self.TIPOS_PRIORIDAD.get(tipo, 1)
        self.tiempo_restante = rafaga
        self.gestiones = gestiones
        self.tiquete = None
        self.estado = "Espera"
        self.tiempo_espera = 0
        self.tiempo_retorno = 0
        self.tiempo_inicio = None
        self.tiempo_fin = None

    def __str__(self):
        return f"ID: {self.id} | {self.nombre} | Tipo: {self.tipo} | Prioridad: {self.prioridad} | Llegada: {self.tiempo_llegada} | Rafaga: {self.rafaga} | Gestiones: {self.gestiones}"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "tiempo_llegada": self.tiempo_llegada,
            "rafaga": self.rafaga,
            "prioridad": self.prioridad,
            "gestiones": self.gestiones,
            "tiempo_restante": self.tiempo_restante,
            "estado": self.estado
        }