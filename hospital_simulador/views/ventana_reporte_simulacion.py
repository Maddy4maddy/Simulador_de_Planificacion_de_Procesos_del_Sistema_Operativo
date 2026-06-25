import tkinter as tk
from styles import EstilosHospital


class VentanaReporteSimulacion:

    def __init__(self, root, resultado):
# Inicializa la ventana del reporte y almacena los resultados producidos por la simulación.
        self.resultado = resultado

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Reporte Final de Simulación")
        self.ventana.geometry("700x500")
        self.ventana.configure(
            bg=EstilosHospital.COLORES["fondo"]
        )

        self.crear_ui()

    def crear_ui(self):
        #Construye la interfaz gráfica del reporte, mostrando las métricas

        EstilosHospital.crear_header(
            self.ventana,
            "REPORTE FINAL DE SIMULACIÓN"
        )

        metricas = self.resultado["metricas"]

        pacientes = self.resultado["pacientes"]

        #Organiza los indicadores principales que serán
        #mostrados al usuario en forma de resumen.
        datos = [
            ("Pacientes atendidos", len(pacientes)),
            ("Tiempo promedio de espera", f"{metricas['espera']:.2f}"),
            ("Tiempo promedio de retorno", f"{metricas['retorno']:.2f}"),
            ("Utilización CPU", f"{metricas['cpu']:.2f}%"),
            ("Tiempo total", metricas["tiempo_total"])
        ]

        #Crea el contenedor principal donde se presentan todas las métricas del reporte.
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

        #Genera dinámicamente una fila para cada métrica calculada durante la simulación.
        for texto, valor in datos:

            fila = tk.Frame(
                frame,
                bg="white"
            )
            fila.pack(
                fill="x",
                pady=8
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

        tk.Button(
            self.ventana,
            text="Cerrar",
            command=self.ventana.destroy
        ).pack(pady=10)