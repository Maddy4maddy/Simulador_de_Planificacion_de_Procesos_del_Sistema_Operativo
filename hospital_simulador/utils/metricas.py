def calcular_metricas(pacientes, tiempo_total):

    if not pacientes or tiempo_total == 0:
        return 0, 0, 0

    total_espera = 0
    total_retorno = 0

    for p in pacientes:
        total_espera += p.tiempo_espera
        total_retorno += p.tiempo_retorno

    promedio_espera = total_espera / len(pacientes)
    promedio_retorno = total_retorno / len(pacientes)

    cpu_utilizacion = (
        sum(p.rafaga for p in pacientes) / tiempo_total
    ) * 100

    return (
        promedio_espera,
        promedio_retorno,
        cpu_utilizacion
    )


def calcular_metricas_desde_gantt(pacientes, gantt):

    if not gantt:
        return {
            "promedio_espera": 0,
            "promedio_retorno": 0,
            "cpu_utilizacion": 0
        }

    datos = {}

    for p in pacientes:

        datos[p.id] = {
            "llegada": p.tiempo_llegada,
            "rafaga": p.rafaga,
            "fin": 0
        }

    for pid, inicio, fin in gantt:

        if pid in datos:
            datos[pid]["fin"] = max(
                datos[pid]["fin"],
                fin
            )

    total_espera = 0
    total_retorno = 0

    for pid, d in datos.items():

        retorno = d["fin"] - d["llegada"]
        espera = retorno - d["rafaga"]

        total_espera += max(0, espera)
        total_retorno += retorno

    n = len(pacientes)

    promedio_espera = total_espera / n
    promedio_retorno = total_retorno / n

    tiempo_total = max(
        fin for _, _, fin in gantt
    )

    cpu_util = (
        sum(p.rafaga for p in pacientes)
        / tiempo_total
    ) * 100

    return {
        "promedio_espera": promedio_espera,
        "promedio_retorno": promedio_retorno,
        "cpu_utilizacion": cpu_util
    }