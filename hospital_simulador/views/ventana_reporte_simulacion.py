import tkinter as tk
from styles import EstilosHospital


class VentanaReporteSimulacion:

    def __init__(self, root, resultado):
        # Inicializa la ventana del reporte y almacena los resultados producidos por la simulación.
        self.resultado = resultado

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Reporte Final de Simulación")
        self.ventana.geometry("700x600")
        self.ventana.configure(
            bg=EstilosHospital.COLORES["fondo"]
        )

        self.crear_ui()

    def crear_ui(self):
        # Construye la interfaz gráfica del reporte.

        EstilosHospital.crear_header(
            self.ventana,
            "REPORTE FINAL DE SIMULACIÓN"
        )

        metricas = self.resultado["metricas"]
        pacientes = self.resultado["pacientes"]

        # Resumen general de la simulación
        datos = [
            ("Pacientes atendidos", len(pacientes)),
            ("Tiempo promedio de espera", f"{metricas['espera']:.2f}"),
            ("Tiempo promedio de retorno", f"{metricas['retorno']:.2f}"),
            ("Utilización CPU", f"{metricas['cpu']:.2f}%"),
            ("Tiempo total", metricas["tiempo_total"])
        ]

        frame = tk.Frame(
            self.ventana,
            bg="white"
        )
        frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Mostrar métricas
        for texto, valor in datos:

            fila = tk.Frame(
                frame,
                bg="white"
            )
            fila.pack(
                fill="x",
                pady=6
            )

            tk.Label(
                fila,
                text=texto + ":",
                width=30,
                anchor="w",
                font=("Segoe UI", 10, "bold"),
                bg="white"
            ).pack(side="left")

            tk.Label(
                fila,
                text=str(valor),
                font=("Segoe UI", 10),
                fg="#8B0000",
                bg="white"
            ).pack(side="left")

        # Separador
        tk.Frame(
            frame,
            bg="#DDDDDD",
            height=2
        ).pack(fill="x", pady=15)

        # Título del detalle
        tk.Label(
            frame,
            text="Detalle de pacientes",
            font=("Segoe UI", 11, "bold"),
            fg="#8B0000",
            bg="white"
        ).pack(anchor="w", pady=(0, 8))

        # Mostrar información de cada paciente
        for p in pacientes:

            texto = (
                f"P{p.id} - {p.nombre} | "
                f"Estado: {p.estado} | "
                f"Espera: {p.tiempo_espera} | "
                f"Retorno: {p.tiempo_retorno}"
            )

            tk.Label(
                frame,
                text=texto,
                bg="white",
                anchor="w",
                justify="left",
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=2)

        tk.Button(
            self.ventana,
            text="Cerrar",
            command=self.ventana.destroy
        ).pack(pady=10)