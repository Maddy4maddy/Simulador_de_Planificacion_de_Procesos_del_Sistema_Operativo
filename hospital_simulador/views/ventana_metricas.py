import tkinter as tk
from styles import EstilosHospital


class VentanaMetricas:

    def __init__(self, root, metricas):

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Métricas del Sistema")
        self.ventana.geometry("600x400")
        self.ventana.configure(bg=EstilosHospital.COLORES["fondo"])

        self.metricas = metricas

        self.crear_ui()

    def crear_ui(self):

        EstilosHospital.crear_header(self.ventana, "MÉTRICAS DE RENDIMIENTO")

        frame = tk.Frame(self.ventana, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        labels = [
            ("Tiempo promedio de espera", self.metricas["espera"]),
            ("Tiempo promedio de retorno", self.metricas["retorno"]),
            ("Utilización CPU (%)", self.metricas["cpu"])
        ]

        for texto, valor in labels:

            card = tk.Frame(frame, bg="#F5F5F5", pady=10, padx=10)
            card.pack(fill="x", pady=10)

            tk.Label(
                card,
                text=texto,
                font=("Segoe UI", 11, "bold"),
                bg="#F5F5F5"
            ).pack(anchor="w")

            tk.Label(
                card,
                text=f"{valor:.2f}",
                font=("Segoe UI", 14),
                fg="#8B0000",
                bg="#F5F5F5"
            ).pack(anchor="w")