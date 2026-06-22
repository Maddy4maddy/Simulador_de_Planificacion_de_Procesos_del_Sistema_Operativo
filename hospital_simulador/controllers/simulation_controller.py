from controllers.mlq_controller import MLQController
from utils.metricas import calcular_metricas

class SimulationController:

    def __init__(self, gestor):
        self.gestor = gestor
        self.mlq = MLQController()

    def ejecutar(self, configuracion, quantum=2):

        pacientes = self.gestor.listar_pacientes()

        if not pacientes:
            return {"error": "No hay pacientes para simular"}

        resultados_mlq = self.mlq.ejecutar(
            pacientes,
            configuracion,
            quantum
        )

        resultado = self._unificar_resultados(resultados_mlq)

        # 🔥 calcular métricas
        tiempo_total = resultado["gantt"][-1][2] if resultado["gantt"] else 0

        promedio_espera, promedio_retorno, cpu = calcular_metricas(
            resultado["pacientes"],
            tiempo_total
        )

        print("\n===== DEBUG =====")

        print("TIEMPO TOTAL:", tiempo_total)

        print(
            "SUMA RAFAGAS:",
            sum(
                p.rafaga
                for p in resultado["pacientes"]
            )
        )

        print("\nGANTT")

        for g in resultado["gantt"]:
            print(g)

        print("=================\n")

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

        # 🔥 FIX IMPORTANTE (SEGURIDAD)
        if resultados_mlq is None:
            return {"error": "MLQ devolvió None"}

        for tipo, data in resultados_mlq.items():

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