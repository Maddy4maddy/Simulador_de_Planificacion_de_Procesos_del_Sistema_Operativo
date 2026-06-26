import tkinter as tk
from tkinter import ttk
from styles import EstilosHospital


class VentanaSimulacionPaso:

    def __init__(
            self,
            root,
            controller,
            ventana_principal,
            configuracion
    ):

        self.controller = controller
        self.ventana_principal = ventana_principal
        self.configuracion = configuracion

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Simulación Paso a Paso")
        self.ventana.geometry("1100x700")
        self.ventana.configure(
            bg=EstilosHospital.COLORES["fondo"]
        )

        self.crear_ui()

    def crear_ui(self):

        EstilosHospital.crear_header(
            self.ventana,
            "SIMULACIÓN PASO A PASO"
        )

        panel_info = tk.Frame(
            self.ventana,
            bg="white",
            relief="solid",
            bd=1
        )
        panel_info.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.label_estado = tk.Label(
            panel_info,
            text="Estado: Listo",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#8B0000"
        )
        self.label_estado.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        self.label_actual = tk.Label(
            panel_info,
            text="Paciente actual: -",
            font=("Segoe UI", 12),
            bg="white"
        )
        self.label_actual.pack(
            anchor="w",
            padx=10
        )

        self.label_estado_paciente = tk.Label(
            panel_info,
            text="Estado del paciente: -",
            font=("Segoe UI", 12),
            bg="white"
        )

        self.label_estado_paciente.pack(
            anchor="w",
            padx=10
        )

        self.label_restante = tk.Label(
            panel_info,
            text="Tiempo restante: -",
            font=("Segoe UI", 12),
            bg="white"
        )

        self.label_restante.pack(
            anchor="w",
            padx=10
        )
        self.label_tiempo = tk.Label(
            panel_info,
            text="Tiempo: 0",
            font=("Segoe UI", 12),
            bg="white"
        )
        self.label_tiempo.pack(
            anchor="w",
            padx=10,
            pady=5
        )

        self.progress = ttk.Progressbar(
            self.ventana,
            orient="horizontal",
            length=500,
            mode="determinate"
        )
        self.progress.pack(
            fill="x",
            padx=15,
            pady=10
        )

        self.btn = tk.Button(
            self.ventana,
            text="▶ Iniciar Simulación",
            font=("Segoe UI", 11, "bold"),
            bg="#8B0000",
            fg="white",
            command=self.iniciar
        )
        self.btn.pack(
            pady=10
        )

        frame_canvas = tk.Frame(
            self.ventana
        )
        frame_canvas.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.canvas = tk.Canvas(
            frame_canvas,
            bg="white"
        )

        scroll_x = ttk.Scrollbar(
            frame_canvas,
            orient="horizontal",
            command=self.canvas.xview
        )

        self.canvas.configure(
            xscrollcommand=scroll_x.set
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        scroll_x.pack(
            fill="x"
        )

    def iniciar(self):

        self.btn.config(state="disabled")

        self.progress["value"] = 0

        configuracion = {
            "Rojo": "FIFO",
            "Amarillo": "SJF",
            "Verde": "RR",
            "Cita": "FIFO",
            "Seguimiento": "RR",
            "Embarazada": "RR"
        }

        gen = self.controller.ejecutar_paso_a_paso(
            configuracion,
            quantum=2
        )

        self.animar(gen)

    def animar(self, gen):

        try:

            timeline, paciente, tiempo = next(gen)

            self.label_estado.config(
                text="Estado: Ejecutando"
            )

            self.label_actual.config(
                text=f"Paciente actual: {paciente.nombre} (P{paciente.id})"
            )

            self.label_estado_paciente.config(
                text=f"Estado del paciente: {paciente.estado}"
            )

            self.label_restante.config(
                text=f"Tiempo restante: {paciente.tiempo_restante}"
            )

            self.label_tiempo.config(
                text=f"Tiempo actual: {tiempo}"
            )

            if timeline:

                ultimo = max(
                    item["fin"]
                    for item in timeline
                )

                self.progress["maximum"] = max(
                    ultimo,
                    1
                )

                self.progress["value"] = tiempo

            self.dibujar(timeline)

            self.ventana.after(
                800,
                lambda: self.animar(gen)
            )

        except StopIteration:

            self.label_estado.config(
                text="Estado: Simulación Finalizada"
            )

            self.label_actual.config(
                text="Paciente actual: Ninguno"
            )

            self.label_estado_paciente.config(
                text="Estado del paciente: Todos atendidos"
            )

            self.label_restante.config(
                text="Tiempo restante: 0"
            )

            self.btn.config(
                state="normal"
            )

    def dibujar(self, timeline):

        self.canvas.delete("all")

        escala = 35
        y = 120
        altura = 60

        colores = [
            "#D32F2F",
            "#1976D2",
            "#388E3C",
            "#F57C00",
            "#7B1FA2",
            "#0097A7",
            "#5D4037"
        ]

        ultimo_tiempo = 0

        for item in timeline:

            ultimo_tiempo = max(
                ultimo_tiempo,
                item["fin"]
            )

        self.canvas.create_text(
            500,
            40,
            text="Ejecución de Procesos",
            font=("Segoe UI", 16, "bold"),
            fill="#8B0000"
        )

        for item in timeline:

            x1 = 50 + item["inicio"] * escala
            x2 = 50 + item["fin"] * escala

            color = colores[
                item["id"] % len(colores)
            ]

            self.canvas.create_rectangle(
                x1,
                y,
                x2,
                y + altura,
                fill=color,
                outline="black",
                width=2
            )

            self.canvas.create_text(
                (x1 + x2) / 2,
                y + 20,
                text=f"P{item['id']}",
                fill="white",
                font=("Segoe UI", 10, "bold")
            )

            self.canvas.create_text(
                (x1 + x2) / 2,
                y + 42,
                text=f"{item['inicio']} - {item['fin']}",
                fill="white",
                font=("Segoe UI", 8)
            )

        self.canvas.create_line(
            50,
            y + altura + 20,
            (ultimo_tiempo + 2) * escala,
            y + altura + 20,
            width=2
        )

        for t in range(ultimo_tiempo + 1):

            x = 50 + t * escala

            self.canvas.create_line(
                x,
                y + altura + 15,
                x,
                y + altura + 25
            )

            self.canvas.create_text(
                x,
                y + altura + 40,
                text=str(t),
                font=("Segoe UI", 8)
            )

        self.canvas.configure(
            scrollregion=(
                0,
                0,
                (ultimo_tiempo + 5) * escala,
                500
            )
        )