from controllers.fifo_controller import FIFOController
from controllers.sjf_controller import SJFController
from controllers.rr_controller import RoundRobinController


class MLQController:

    def __init__(self):
        self.fifo = FIFOController()
        self.sjf = SJFController()
        self.rr = RoundRobinController()

    def separar_colas(self, pacientes):

        colas = {
            "Rojo": [],
            "Amarillo": [],
            "Embarazada": [],
            "Verde": [],
            "Cita": [],
            "Seguimiento": []
        }

        for paciente in pacientes:
            colas[paciente.tipo].append(paciente)

        return colas

    def ejecutar(self, pacientes, configuracion, quantum=2):

        colas = self.separar_colas(pacientes)

        resultados = {}

        tiempo_global = 0

        orden_prioridad = [
            "Rojo",
            "Amarillo",
            "Embarazada",
            "Verde",
            "Cita",
            "Seguimiento"
        ]

        for tipo in orden_prioridad:

            lista_pacientes = colas[tipo]

            if not lista_pacientes:
                continue

            algoritmo = configuracion.get(tipo, "FIFO")

            if algoritmo == "FIFO":

                resultado = self.fifo.ejecutar(
                    lista_pacientes
                )

            elif algoritmo == "SJF":

                resultado = self.sjf.ejecutar(
                    lista_pacientes
                )

            elif algoritmo == "RR":

                resultado = self.rr.ejecutar(
                    lista_pacientes,
                    quantum
                )

            else:

                raise ValueError(
                    f"Algoritmo no válido para {tipo}"
                )

            gantt_ajustado = []

            for pid, inicio, fin in resultado["gantt"]:

                gantt_ajustado.append(
                    (
                        pid,
                        inicio + tiempo_global,
                        fin + tiempo_global
                    )
                )

            resultado["gantt"] = gantt_ajustado

            for paciente in resultado["pacientes"]:

                if paciente.tiempo_inicio is not None:
                    paciente.tiempo_inicio += tiempo_global

                if paciente.tiempo_fin is not None:
                    paciente.tiempo_fin += tiempo_global

                paciente.tiempo_retorno = (
                    paciente.tiempo_fin -
                    paciente.tiempo_llegada
                )

                paciente.tiempo_espera = (
                    paciente.tiempo_retorno -
                    paciente.rafaga
                )

            if gantt_ajustado:
                tiempo_global = max(
                    fin
                    for _, _, fin in gantt_ajustado
                )

            resultados[tipo] = resultado

        return resultados