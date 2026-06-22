import tkinter as tk
from tkinter import ttk
from styles import EstilosHospital


class VentanaGantt:

    def __init__(self, root, gantt_data):

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Diagrama de Gantt - MLQ")
        self.ventana.geometry("1100x650")
        self.ventana.configure(
            bg=EstilosHospital.COLORES["fondo"]
        )

        self.gantt_data = gantt_data

        self.crear_ui()

    def crear_ui(self):

        EstilosHospital.crear_header(
            self.ventana,
            "DIAGRAMA DE GANTT"
        )

        frame = tk.Frame(
            self.ventana,
            bg=EstilosHospital.COLORES["fondo"]
        )
        frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        info = tk.Label(
            frame,
            text=f"Procesos ejecutados: {len(self.gantt_data)}",
            font=("Segoe UI", 11, "bold"),
            bg=EstilosHospital.COLORES["fondo"],
            fg="#8B0000"
        )
        info.pack(pady=5)

        canvas_frame = tk.Frame(
            frame,
            bg=EstilosHospital.COLORES["fondo"]
        )
        canvas_frame.pack(
            fill="both",
            expand=True
        )

        self.canvas = tk.Canvas(
            canvas_frame,
            bg="white",
            height=400
        )

        scrollbar_x = ttk.Scrollbar(
            canvas_frame,
            orient="horizontal",
            command=self.canvas.xview
        )

        scrollbar_y = ttk.Scrollbar(
            canvas_frame,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            xscrollcommand=scrollbar_x.set,
            yscrollcommand=scrollbar_y.set
        )

        self.canvas.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar_y.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scrollbar_x.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        canvas_frame.grid_rowconfigure(
            0,
            weight=1
        )

        canvas_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.dibujar_gantt()

    def dibujar_gantt(self):

        if not self.gantt_data:
            return

        escala = 35
        altura = 70
        y = 120

        colores = [
            "#D32F2F",
            "#1976D2",
            "#388E3C",
            "#F57C00",
            "#7B1FA2",
            "#0097A7",
            "#5D4037",
            "#455A64"
        ]

        ultimo_tiempo = max(
            fin for _, _, fin in self.gantt_data
        )

        self.canvas.create_text(
            550,
            40,
            text="Planificación de Procesos",
            font=("Segoe UI", 16, "bold"),
            fill="#8B0000"
        )

        self.canvas.create_line(
            40,
            y + altura + 20,
            ultimo_tiempo * escala + 80,
            y + altura + 20,
            width=2
        )

        for tiempo in range(ultimo_tiempo + 1):

            x = 40 + tiempo * escala

            self.canvas.create_line(
                x,
                y + altura + 15,
                x,
                y + altura + 25
            )

            self.canvas.create_text(
                x,
                y + altura + 40,
                text=str(tiempo),
                font=("Segoe UI", 8)
            )

        for i, item in enumerate(self.gantt_data):

            pid, inicio, fin = item

            x1 = 40 + inicio * escala
            x2 = 40 + fin * escala

            color = colores[pid % len(colores)]

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
                y + 25,
                text=f"P{pid}",
                fill="white",
                font=("Segoe UI", 10, "bold")
            )

            self.canvas.create_text(
                (x1 + x2) / 2,
                y + 50,
                text=f"{inicio}-{fin}",
                fill="white",
                font=("Segoe UI", 8)
            )

        tiempo_total = ultimo_tiempo

        panel = tk.Frame(
            self.ventana,
            bg="white",
            relief="solid",
            bd=1
        )
        panel.pack(
            fill="x",
            padx=15,
            pady=10
        )

        tk.Label(
            panel,
            text=f"Tiempo Total: {tiempo_total}",
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg="#8B0000"
        ).pack(
            side="left",
            padx=20,
            pady=10
        )

        tk.Label(
            panel,
            text=f"Bloques Ejecutados: {len(self.gantt_data)}",
            font=("Segoe UI", 11, "bold"),
            bg="white"
        ).pack(
            side="left",
            padx=20
        )

        self.canvas.configure(
            scrollregion=(
                0,
                0,
                (ultimo_tiempo + 5) * escala,
                500
            )
        )