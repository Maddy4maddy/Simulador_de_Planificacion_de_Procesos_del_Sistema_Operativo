import os
from datetime import datetime


class HistorialController:

    RUTA_PACIENTES = "data/historial_pacientes.txt"
    RUTA_EJECUCIONES = "data/historial_ejecuciones.txt"

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self._inicializar_archivo(
            self.RUTA_PACIENTES,
            "# ejecucion_id|fecha|id_paciente|nombre|tipo|prioridad|llegada|rafaga|gestiones|tiempo_espera|tiempo_retorno\n"
        )
        self._inicializar_archivo(
            self.RUTA_EJECUCIONES,
            "# ejecucion_id|fecha|algoritmo|total_pacientes|prom_espera|prom_retorno|cpu_utilizacion|tiempo_total\n"
        )

    def guardar_simulacion(self, pacientes, metricas, algoritmo="MLQ"):
        ejecucion_id = datetime.now().strftime("EJC-%Y%m%d-%H%M%S")
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.RUTA_PACIENTES, "a", encoding="utf-8") as f:
            for p in pacientes:
                f.write(
                    f"{ejecucion_id}|{fecha}|{p.id}|{p.nombre}|{p.tipo}"
                    f"|{p.prioridad}|{p.tiempo_llegada}|{p.rafaga}"
                    f"|{p.gestiones}|{p.tiempo_espera:.2f}|{p.tiempo_retorno:.2f}\n"
                )

        with open(self.RUTA_EJECUCIONES, "a", encoding="utf-8") as f:
            f.write(
                f"{ejecucion_id}|{fecha}|{algoritmo}|{len(pacientes)}"
                f"|{metricas.get('espera', 0):.2f}"
                f"|{metricas.get('retorno', 0):.2f}"
                f"|{metricas.get('cpu', 0):.2f}"
                f"|{metricas.get('tiempo_total', 0)}\n"
            )

        return ejecucion_id

    def obtener_ejecuciones(self):
        return self._leer_archivo(
            self.RUTA_EJECUCIONES,
            ["ejecucion_id", "fecha", "algoritmo", "total_pacientes",
             "prom_espera", "prom_retorno", "cpu_utilizacion", "tiempo_total"]
        )

    def obtener_pacientes_de_ejecucion(self, ejecucion_id):
        todos = self._leer_archivo(
            self.RUTA_PACIENTES,
            ["ejecucion_id", "fecha", "id_paciente", "nombre", "tipo",
             "prioridad", "llegada", "rafaga", "gestiones",
             "tiempo_espera", "tiempo_retorno"]
        )
        return [r for r in todos if r["ejecucion_id"] == ejecucion_id]

    def obtener_todos_los_pacientes(self):
        return self._leer_archivo(
            self.RUTA_PACIENTES,
            ["ejecucion_id", "fecha", "id_paciente", "nombre", "tipo",
             "prioridad", "llegada", "rafaga", "gestiones",
             "tiempo_espera", "tiempo_retorno"]
        )

    def calcular_estadisticas_historicas(self):
        ejecuciones = self.obtener_ejecuciones()
        pacientes = self.obtener_todos_los_pacientes()

        if not ejecuciones:
            return {
                "total_ejecuciones": 0,
                "total_pacientes": 0,
                "prom_espera_global": 0.0,
                "prom_retorno_global": 0.0,
                "prom_cpu_global": 0.0,
                "gestiones_por_tipo": {}
            }

        prom_espera = sum(float(e["prom_espera"]) for e in ejecuciones) / len(ejecuciones)
        prom_retorno = sum(float(e["prom_retorno"]) for e in ejecuciones) / len(ejecuciones)
        prom_cpu = sum(float(e["cpu_utilizacion"]) for e in ejecuciones) / len(ejecuciones)

        gestiones_por_tipo = {}
        for p in pacientes:
            tipo = p["tipo"]
            gestiones = int(p.get("gestiones", 1))
            gestiones_por_tipo[tipo] = gestiones_por_tipo.get(tipo, 0) + gestiones

        return {
            "total_ejecuciones": len(ejecuciones),
            "total_pacientes": len(pacientes),
            "prom_espera_global": round(prom_espera, 2),
            "prom_retorno_global": round(prom_retorno, 2),
            "prom_cpu_global": round(prom_cpu, 2),
            "gestiones_por_tipo": gestiones_por_tipo
        }

    def _inicializar_archivo(self, ruta, header):
        if not os.path.exists(ruta):
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(header)

    def _leer_archivo(self, ruta, columnas):
        registros = []
        if not os.path.exists(ruta):
            return registros
        with open(ruta, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith("#"):
                    continue
                partes = linea.split("|")
                if len(partes) < len(columnas):
                    continue
                registros.append(dict(zip(columnas, partes)))
        return registros