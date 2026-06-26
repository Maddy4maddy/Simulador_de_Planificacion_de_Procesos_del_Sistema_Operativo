import copy


class SimulationStepController:

    def __init__(self, gestor):
        self.gestor = gestor

    def ejecutar_paso_a_paso(self, configuracion, quantum=2):

        pacientes = copy.deepcopy(
            self.gestor.listar_pacientes_disponibles()
        )

        if not pacientes:
            return

        timeline = []
        tiempo_actual = 0

        while pacientes:

            pacientes.sort(
                key=lambda p: p.tiempo_llegada
            )

            paciente = pacientes.pop(0)

            if tiempo_actual < paciente.tiempo_llegada:
                tiempo_actual = paciente.tiempo_llegada

            if paciente.tiempo_inicio is None:
                paciente.tiempo_inicio = tiempo_actual

            paciente.iniciar_atencion()

            ejecucion = min(
                quantum,
                paciente.tiempo_restante
            )

            inicio = tiempo_actual
            tiempo_actual += ejecucion
            fin = tiempo_actual

            paciente.tiempo_restante -= ejecucion

            timeline.append({
                "id": paciente.id,
                "nombre": paciente.nombre,
                "inicio": inicio,
                "fin": fin,
                "restante": paciente.tiempo_restante,
                "estado": paciente.estado
            })

            paciente_real = self.gestor.buscar_por_id(
                paciente.id
            )

            if paciente_real:

                paciente_real.estado = paciente.estado
                paciente_real.tiempo_restante = paciente.tiempo_restante

            if paciente.tiempo_restante <= 0:

                paciente.tiempo_fin = fin

                paciente.tiempo_retorno = (
                    paciente.tiempo_fin -
                    paciente.tiempo_llegada
                )

                paciente.tiempo_espera = (
                    paciente.tiempo_retorno -
                    paciente.rafaga
                )

                paciente.finalizar_atencion()

                if paciente_real:

                    paciente_real.tiempo_inicio = paciente.tiempo_inicio
                    paciente_real.tiempo_fin = paciente.tiempo_fin
                    paciente_real.tiempo_espera = paciente.tiempo_espera
                    paciente_real.tiempo_retorno = paciente.tiempo_retorno
                    paciente_real.tiempo_restante = 0
                    paciente_real.finalizar_atencion()

            else:

                pacientes.append(paciente)

            yield timeline, paciente, tiempo_actual