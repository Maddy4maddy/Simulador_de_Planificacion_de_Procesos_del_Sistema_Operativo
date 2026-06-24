from controllers.fifo_controller import FIFOController
from controllers.sjf_controller import SJFController
from controllers.rr_controller import RoundRobinController
from controllers.mlq_controller import MLQController
from utils.metricas import calcular_metricas_desde_gantt
import copy

class ComparadorController:

    def __init__(self):
        self.fifo = FIFOController()
        self.sjf = SJFController()
        self.rr = RoundRobinController()
        self.mlq = MLQController()

    def ejecutar_comparacion(self, pacientes, quantum=2):

        resultados = {}

        # ======================
        # FIFO
        # ======================
        r_fifo = self.fifo.ejecutar(
        copy.deepcopy(pacientes)
        )
        resultados["FIFO"] = self._resumen(r_fifo, pacientes)

        # ======================
        # SJF
        # ======================
        r_sjf = self.sjf.ejecutar(
            copy.deepcopy(pacientes)
        )
        resultados["SJF"] = self._resumen(r_sjf, pacientes)

        # ======================
        # RR
        # ======================
        r_rr = self.rr.ejecutar(
            copy.deepcopy(pacientes),
            quantum
        )
        resultados["RR"] = self._resumen(r_rr, pacientes)

        # ======================
        # MLQ
        # ======================
        configuracion = {
            "Rojo": "FIFO",
            "Amarillo": "SJF",
            "Embarazada": "RR",
            "Verde": "FIFO",
            "Cita": "SJF",
            "Seguimiento": "FIFO"
        }

        r_mlq = self.mlq.ejecutar(
            copy.deepcopy(pacientes),
            configuracion,
            quantum
        )
        gantt_mlq = []

        for data in r_mlq.values():
            gantt_mlq.extend(data["gantt"])

        gantt_mlq.sort(key=lambda x: x[1])

        resultados["MLQ"] = self._resumen({"gantt": gantt_mlq}, pacientes)

        return resultados

    def _resumen(self, resultado, pacientes):

        gantt = resultado["gantt"]

        metricas = calcular_metricas_desde_gantt(pacientes, gantt)

        return {
            "promedio_espera": metricas["promedio_espera"],
            "promedio_retorno": metricas["promedio_retorno"],
            "cpu_utilizacion": metricas["cpu_utilizacion"],
            "tiempo_total": max(g[2] for g in gantt),
             "gantt": gantt
        }