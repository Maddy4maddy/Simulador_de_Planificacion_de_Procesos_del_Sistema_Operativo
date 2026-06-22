import time
import copy


class SimulationStepController:

    def __init__(self, gestor):
        self.gestor = gestor

    def ejecutar_paso_a_paso(self, configuracion, quantum=2):

        pacientes = copy.deepcopy(self.gestor.listar_pacientes())

        timeline = []
        tiempo_actual = 0

        while pacientes:

            # ordenar por llegada simple (base)
            pacientes.sort(key=lambda p: p.tiempo_llegada)

            paciente = pacientes.pop(0)

            ejecucion = min(paciente.tiempo_restante, quantum)

            inicio = tiempo_actual
            fin = tiempo_actual + ejecucion

            paciente.tiempo_restante -= ejecucion
            tiempo_actual = fin

            timeline.append({
                "id": paciente.id,
                "nombre": paciente.nombre,
                "inicio": inicio,
                "fin": fin,
                "restante": paciente.tiempo_restante
            })

            if paciente.tiempo_restante > 0:
                pacientes.append(paciente)

            yield timeline, paciente, tiempo_actual