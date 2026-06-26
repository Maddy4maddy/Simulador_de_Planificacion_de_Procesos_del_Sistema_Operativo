from controllers.mlq_controller import MLQController
from utils.metricas import calcular_metricas


class SimulationController:

    def __init__(self, gestor):
        self.gestor = gestor
        self.mlq = MLQController()

    def ejecutar(self, configuracion, quantum=2):

        # Solo pacientes pendientes
        pacientes = self.gestor.listar_pacientes_disponibles()

        if not pacientes:
            return {
                "error": "No hay pacientes pendientes para simular"
            }

        # Reiniciar métricas para una nueva simulación
        for paciente in pacientes:
            paciente.tiempo_restante = paciente.rafaga
            paciente.tiempo_inicio = None
            paciente.tiempo_fin = None
            paciente.tiempo_espera = 0
            paciente.tiempo_retorno = 0

        resultados_mlq = self.mlq.ejecutar(
            pacientes,
            configuracion,
            quantum
        )

        resultado = self._unificar_resultados(resultados_mlq)

        tiempo_total = (
            resultado["gantt"][-1][2]
            if resultado["gantt"]
            else 0
        )

        promedio_espera, promedio_retorno, cpu = calcular_metricas(
            resultado["pacientes"],
            tiempo_total
        )

        resultado["metricas"] = {
            "espera": promedio_espera,
            "retorno": promedio_retorno,
            "cpu": cpu,
            "tiempo_total": tiempo_total
        }

        return resultado

    def _unificar_resultados(self, resultados_mlq):

        gantt_global = []
        pacientes_finales = []

        if resultados_mlq is None:
            return {
                "error": "MLQ devolvió None"
            }

        for _, data in resultados_mlq.items():

            if not data:
                continue

            gantt_global.extend(data.get("gantt", []))
            pacientes_finales.extend(data.get("pacientes", []))

        gantt_global.sort(key=lambda x: x[1])

        return {
            "algoritmo": "MLQ",
            "pacientes": pacientes_finales,
            "gantt": gantt_global
        }