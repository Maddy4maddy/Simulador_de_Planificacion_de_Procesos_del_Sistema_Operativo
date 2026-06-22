import tkinter as tk
from styles import EstilosHospital


class VentanaComparacion:

    def __init__(self, root, datos):

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Comparación de Algoritmos")
        self.ventana.geometry("900x500")
        self.ventana.configure(bg=EstilosHospital.COLORES["fondo"])

        self.datos = datos

        self.crear_ui()

    def crear_ui(self):

        EstilosHospital.crear_header(self.ventana, "COMPARACIÓN DE ALGORITMOS")

        frame = tk.Frame(self.ventana, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        for alg, data in self.datos.items():

            card = tk.Frame(frame, bg="#F5F5F5", pady=10, padx=10)
            card.pack(fill="x", pady=10)

            tk.Label(
                card,
                text=alg,
                font=("Segoe UI", 14, "bold"),
                bg="#F5F5F5",
                fg="#8B0000"
            ).pack(anchor="w")

            tk.Label(card,
                text=f"Espera promedio: {data['promedio_espera']:.2f}"
            ).pack(anchor="w")

            tk.Label(card,
                text=f"Retorno promedio: {data['promedio_retorno']:.2f}"
            ).pack(anchor="w")

            tk.Label(card,
                text=f"CPU: {data['cpu_utilizacion']:.2f}%"
            ).pack(anchor="w")

            tk.Label(card,
                text=f"Tiempo total: {data['tiempo_total']}"
            ).pack(anchor="w")