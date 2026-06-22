from utils.metricas import calcular_metricas
import copy

class FIFOController:

    def ejecutar(self, pacientes):

        pacientes = copy.deepcopy(pacientes)

        pacientes = sorted(
            pacientes,
            key=lambda p: p.tiempo_llegada
        )

        tiempo_actual = 0
        gantt = []

        for paciente in pacientes:

            if tiempo_actual < paciente.tiempo_llegada:
                tiempo_actual = paciente.tiempo_llegada

            paciente.tiempo_inicio = tiempo_actual
            paciente.tiempo_espera = tiempo_actual - paciente.tiempo_llegada

            tiempo_actual += paciente.rafaga

            paciente.tiempo_fin = tiempo_actual
            paciente.tiempo_retorno = (
                paciente.tiempo_fin -
                paciente.tiempo_llegada
            )

            gantt.append(
                (
                    paciente.id,
                    paciente.tiempo_inicio,
                    paciente.tiempo_fin
                )
            )

        promedio_espera, promedio_retorno, cpu = calcular_metricas(
            pacientes,
            tiempo_actual
        )

        return {
            "algoritmo": "FIFO",
            "pacientes": pacientes,
            "gantt": gantt,
            "tiempo_total": tiempo_actual,
            "promedio_espera": promedio_espera,
            "promedio_retorno": promedio_retorno,
            "cpu_utilizacion": cpu
        }