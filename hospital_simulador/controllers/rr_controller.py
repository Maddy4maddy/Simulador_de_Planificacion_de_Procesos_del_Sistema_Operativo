from collections import deque
from utils.metricas import calcular_metricas
import copy

class RoundRobinController:

    def ejecutar(self, pacientes, quantum):

        pacientes = copy.deepcopy(pacientes)

        cola = deque(
            sorted(
                pacientes,
                key=lambda p: p.tiempo_llegada
            )
        )
        tiempo_actual = 0
        gantt = []
        completados = []

        while cola:

            paciente = cola.popleft()

            # si el proceso llega después, se avanza el tiempo
            if tiempo_actual < paciente.tiempo_llegada:
                tiempo_actual = paciente.tiempo_llegada

            # primera vez que entra CPU
            if paciente.tiempo_inicio is None:
                paciente.tiempo_inicio = tiempo_actual

            # ejecutar quantum o lo que falte
            ejecucion = min(quantum, paciente.tiempo_restante)

            inicio = tiempo_actual
            tiempo_actual += ejecucion
            fin = tiempo_actual

            paciente.tiempo_restante -= ejecucion

            gantt.append((paciente.id, inicio, fin))

            # si no termina, vuelve a la cola
            if paciente.tiempo_restante > 0:
                cola.append(paciente)
            else:
                paciente.tiempo_fin = tiempo_actual
                paciente.tiempo_retorno = paciente.tiempo_fin - paciente.tiempo_llegada
                paciente.tiempo_espera = paciente.tiempo_retorno - paciente.rafaga
                completados.append(paciente)

        promedio_espera, promedio_retorno, cpu = calcular_metricas(
            completados, tiempo_actual
        )

        return {
            "algoritmo": "ROUND ROBIN",
            "pacientes": completados,
            "gantt": gantt,
            "tiempo_total": tiempo_actual,
            "promedio_espera": promedio_espera,
            "promedio_retorno": promedio_retorno,
            "cpu_utilizacion": cpu
        }