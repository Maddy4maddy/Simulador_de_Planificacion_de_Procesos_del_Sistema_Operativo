import tkinter as tk
from tkinter import ttk
from styles import EstilosHospital


class VentanaReporte:

    def __init__(self, root, historial_controller):
        self.historial = historial_controller

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Reporte Final de Simulación")
        self.ventana.geometry("700x550")
        self.ventana.configure(bg=EstilosHospital.COLORES["fondo"])

        self.crear_ui()

    def crear_ui(self):
        EstilosHospital.crear_header(self.ventana, "REPORTE HISTÓRICO GLOBAL")

        stats = self.historial.calcular_estadisticas_historicas()

        frame_resumen = tk.LabelFrame(
            self.ventana,
            text="Resumen general",
            font=("Segoe UI", 10, "bold"),
            fg=EstilosHospital.COLORES["rojo_principal"],
            bg=EstilosHospital.COLORES["fondo"],
            padx=15,
            pady=10
        )
        frame_resumen.pack(fill="x", padx=20, pady=15)

        datos_resumen = [
            ("Total de ejecuciones", stats["total_ejecuciones"]),
            ("Total de pacientes atendidos", stats["total_pacientes"]),
            ("Promedio de espera global", f"{stats['prom_espera_global']:.2f} min"),
            ("Promedio de retorno global", f"{stats['prom_retorno_global']:.2f} min"),
            ("Utilización de CPU promedio", f"{stats['prom_cpu_global']:.2f} %"),
        ]

        for etiqueta, valor in datos_resumen:
            fila = tk.Frame(frame_resumen, bg=EstilosHospital.COLORES["fondo"])
            fila.pack(fill="x", pady=3)

            tk.Label(
                fila,
                text=etiqueta + ":",
                font=("Segoe UI", 10, "bold"),
                bg=EstilosHospital.COLORES["fondo"],
                fg=EstilosHospital.COLORES["texto_oscuro"],
                width=30,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                fila,
                text=str(valor),
                font=("Segoe UI", 10),
                bg=EstilosHospital.COLORES["fondo"],
                fg=EstilosHospital.COLORES["rojo_principal"]
            ).pack(side="left")

        frame_gestiones = tk.LabelFrame(
            self.ventana,
            text="Gestiones por tipo de paciente",
            font=("Segoe UI", 10, "bold"),
            fg=EstilosHospital.COLORES["rojo_principal"],
            bg=EstilosHospital.COLORES["fondo"],
            padx=15,
            pady=10
        )
        frame_gestiones.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        cols = ("Tipo de Paciente", "Total Gestiones")
        tree = ttk.Treeview(frame_gestiones, columns=cols, show="headings", height=7)
        tree.heading("Tipo de Paciente", text="TIPO DE PACIENTE")
        tree.heading("Total Gestiones", text="TOTAL GESTIONES")
        tree.column("Tipo de Paciente", width=250, anchor="center")
        tree.column("Total Gestiones", width=200, anchor="center")

        orden = ["Rojo", "Amarillo", "Embarazada", "Verde", "Cita", "Seguimiento"]
        gestiones = stats.get("gestiones_por_tipo", {})

        for tipo in orden:
            total = gestiones.get(tipo, 0)
            tree.insert("", "end", values=(tipo, total))

        tree.pack(fill="both", expand=True)

        tk.Button(
            self.ventana,
            text="Cerrar",
            command=self.ventana.destroy,
            bg=EstilosHospital.COLORES["gris"],
            fg="white",
            font=("Segoe UI", 10),
            padx=20,
            pady=6,
            relief="raised",
            bd=2,
            activebackground=EstilosHospital.COLORES["gris_hover"],
            activeforeground="white",
            cursor="hand2"
        ).pack(pady=10)