import tkinter as tk
from tkinter import ttk
from styles import EstilosHospital


class VentanaComparacion:

    def __init__(self, root, datos):
        self.ventana = tk.Toplevel(root)
        self.ventana.title("Comparación de Algoritmos")
        self.ventana.geometry("1000x650")
        self.ventana.configure(bg=EstilosHospital.COLORES["fondo"])

        self.datos = datos
        self.crear_ui()

    def crear_ui(self):
        EstilosHospital.crear_header(self.ventana, "COMPARACIÓN DE ALGORITMOS")

        notebook = ttk.Notebook(self.ventana)
        notebook.pack(fill="both", expand=True, padx=15, pady=10)

        self._crear_tab_resumen(notebook)

        for algoritmo, data in self.datos.items():
            if "gantt" in data:
                self._crear_tab_gantt(notebook, algoritmo, data["gantt"])

    def _crear_tab_resumen(self, notebook):
        frame = tk.Frame(notebook, bg="white")
        notebook.add(frame, text="Resumen General")

        canvas_scroll = tk.Canvas(frame, bg="white")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas_scroll.yview)
        canvas_scroll.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas_scroll.pack(side="left", fill="both", expand=True)

        interior = tk.Frame(canvas_scroll, bg="white")
        canvas_scroll.create_window((0, 0), window=interior, anchor="nw")
        interior.bind("<Configure>", lambda e: canvas_scroll.configure(
            scrollregion=canvas_scroll.bbox("all")))

        colores_alg = {
            "FIFO":"#1976D2",
            "SJF":"#388E3C",
            "RR": "#F57C00",
            "MLQ":"#8B0000"
        }

        for alg, data in self.datos.items():
            color = colores_alg.get(alg, "#555555")

            card = tk.Frame(interior, bg="#F5F5F5", pady=12, padx=15,
                            relief="solid", bd=1)
            card.pack(fill="x", padx=20, pady=8)

            tk.Label(
                card, text=alg,
                font=("Segoe UI", 14, "bold"),
                bg="#F5F5F5", fg=color
            ).pack(anchor="w")

            separador = tk.Frame(card, height=2, bg=color)
            separador.pack(fill="x", pady=5)

            fila = tk.Frame(card, bg="#F5F5F5")
            fila.pack(fill="x")

            metricas = [
                ("Espera promedio", f"{data['promedio_espera']:.2f} min"),
                ("Retorno promedio",f"{data['promedio_retorno']:.2f} min"),
                ("Utilización CPU", f"{data['cpu_utilizacion']:.2f} %"),
                ("Tiempo total", f"{data['tiempo_total']} min"),
            ]

            for etiqueta, valor in metricas:
                bloque = tk.Frame(fila, bg="#F5F5F5", padx=15)
                bloque.pack(side="left")

                tk.Label(bloque, text=etiqueta,
                         font=("Segoe UI", 9),
                         bg="#F5F5F5", fg="#555555").pack(anchor="w")

                tk.Label(bloque, text=valor,
                         font=("Segoe UI", 12, "bold"),
                         bg="#F5F5F5", fg=color).pack(anchor="w")

    def _crear_tab_gantt(self, notebook, algoritmo, gantt_data):
        frame = tk.Frame(notebook, bg=EstilosHospital.COLORES["fondo"])
        notebook.add(frame, text=f"Gantt {algoritmo}")

        if not gantt_data:
            tk.Label(frame, text="Sin datos de ejecución",
                     font=("Segoe UI", 11),
                     bg=EstilosHospital.COLORES["fondo"],
                     fg="#888888").pack(expand=True)
            return

        info = tk.Label(
            frame,
            text=f"Secuencia de ejecución — {algoritmo}  ({len(gantt_data)} bloques)",
            font=("Segoe UI", 11, "bold"),
            bg=EstilosHospital.COLORES["fondo"],
            fg=EstilosHospital.COLORES["rojo_principal"]
        )
        info.pack(pady=8)

        canvas_frame = tk.Frame(frame, bg=EstilosHospital.COLORES["fondo"])
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg="white", height=300)
        scroll_x = ttk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
        scroll_y = ttk.Scrollbar(canvas_frame, orient="vertical",   command=canvas.yview)
        canvas.configure(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        canvas.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        escala  = 35
        altura  = 60
        y_base  = 80
        colores = ["#D32F2F","#1976D2","#388E3C","#F57C00",
                   "#7B1FA2","#0097A7","#5D4037","#455A64"]

        ultimo_tiempo = max(fin for _, _, fin in gantt_data)

        canvas.create_line(
            40, y_base + altura + 20,
            ultimo_tiempo * escala + 80, y_base + altura + 20,
            width=2
        )

        for t in range(ultimo_tiempo + 1):
            x = 40 + t * escala
            canvas.create_line(x, y_base + altura + 15, x, y_base + altura + 25)
            canvas.create_text(x, y_base + altura + 38,
                               text=str(t), font=("Segoe UI", 8))

        for pid, inicio, fin in gantt_data:
            x1 = 40 + inicio * escala
            x2 = 40 + fin    * escala
            color = colores[pid % len(colores)]

            canvas.create_rectangle(x1, y_base, x2, y_base + altura,
                                    fill=color, outline="black", width=2)
            canvas.create_text((x1 + x2) / 2, y_base + 22,
                               text=f"P{pid}", fill="white",
                               font=("Segoe UI", 10, "bold"))
            canvas.create_text((x1 + x2) / 2, y_base + 44,
                               text=f"{inicio}-{fin}", fill="white",
                               font=("Segoe UI", 8))

        canvas.configure(scrollregion=(0, 0, (ultimo_tiempo + 5) * escala, 300))

        panel = tk.Frame(frame, bg="white", relief="solid", bd=1)
        panel.pack(fill="x", padx=15, pady=8)

        tk.Label(panel, text=f"Tiempo total: {ultimo_tiempo}",
                 font=("Segoe UI", 10, "bold"),
                 bg="white", fg=EstilosHospital.COLORES["rojo_principal"]
                 ).pack(side="left", padx=20, pady=6)

        tk.Label(panel, text=f"Bloques ejecutados: {len(gantt_data)}",
                 font=("Segoe UI", 10, "bold"),
                 bg="white").pack(side="left", padx=20)