from datetime import datetime

class Tiquete:
    contador = 1

    def __init__(self, paciente):
        self.numero = Tiquete.contador
        Tiquete.contador += 1
        self.paciente = paciente
        self.fecha_emision = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.estado = "Espera"
        self.tiempo_espera = 0
        self.tiempo_atencion = 0
        paciente.tiquete = self

    def __str__(self):
        return f"Tiquete #{self.numero:04d} - {self.paciente.nombre} - Estado: {self.estado}"

    def iniciar_atencion(self):
        self.estado = "Atencion"

    def finalizar_atencion(self):
        self.estado = "Finalizado"

    def to_dict(self):
        return {
            "numero": self.numero,
            "paciente_id": self.paciente.id,
            "fecha_emision": self.fecha_emision,
            "estado": self.estado,
            "tiempo_espera": self.tiempo_espera,
            "tiempo_atencion": self.tiempo_atencion
        }