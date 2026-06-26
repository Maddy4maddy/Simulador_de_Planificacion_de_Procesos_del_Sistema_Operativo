from utils.metricas import calcular_metricas
import copy


class SJFController:

    def ejecutar(self, pacientes):

        pacientes = copy.deepcopy(pacientes)

        tiempo_actual = 0
        gantt = []

        pacientes = sorted(
            pacientes,
            key=lambda p: p.tiempo_llegada
        )

        completados = []
        lista = pacientes[:]

        while lista:

            disponibles = [
                p for p in lista
                if p.tiempo_llegada <= tiempo_actual
            ]

            if not disponibles:
                tiempo_actual += 1
                continue

            actual = min(
                disponibles,
                key=lambda p: p.rafaga
            )

            if tiempo_actual < actual.tiempo_llegada:
                tiempo_actual = actual.tiempo_llegada

            actual.iniciar_atencion()

            actual.tiempo_inicio = tiempo_actual

            actual.tiempo_espera = (
                tiempo_actual -
                actual.tiempo_llegada
            )

            tiempo_actual += actual.rafaga

            actual.tiempo_fin = tiempo_actual

            actual.tiempo_retorno = (
                actual.tiempo_fin -
                actual.tiempo_llegada
            )

            actual.tiempo_restante = 0

            actual.finalizar_atencion()

            gantt.append(
                (
                    actual.id,
                    actual.tiempo_inicio,
                    actual.tiempo_fin
                )
            )

            completados.append(actual)

            lista.remove(actual)

        promedio_espera, promedio_retorno, cpu = calcular_metricas(
            completados,
            tiempo_actual
        )

        return {
            "algoritmo": "SJF",
            "pacientes": completados,
            "gantt": gantt,
            "tiempo_total": tiempo_actual,
            "promedio_espera": promedio_espera,
            "promedio_retorno": promedio_retorno,
            "cpu_utilizacion": cpu
        }