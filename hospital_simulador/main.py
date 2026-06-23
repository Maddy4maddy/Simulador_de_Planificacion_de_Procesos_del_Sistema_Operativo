import tkinter as tk
from controllers.gestor_pacientes import GestorPacientes
from controllers.simulation_controller import SimulationController
from controllers.comparador_controller import ComparadorController
from views import VentanaPrincipal
import os


class App:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Sistema de Gestion Hospitalaria - Hospital Dr. Maximiliano Peralta Jiménez")
        self.root.geometry("1200x750")
        self.root.resizable(True, True)

        # BACKEND
        self.gestor = GestorPacientes()
        self.archivo_actual = "data/pacientes_registrados.txt"

        self.simulation = SimulationController(self.gestor)
        self.comparador = ComparadorController()

        self.cargar_archivo_inicio()

        # FRONTEND
        self.ventana_principal = VentanaPrincipal(
            self.root,
            self.gestor,
            self.archivo_actual,
            self.simulation,
            self.comparador
        )

        self.ventana_principal.actualizar_lista()

    def cargar_archivo_inicio(self):
        try:
            if os.path.exists(self.archivo_actual):
                self.gestor.cargar_desde_txt(self.archivo_actual)

                print("DEBUG MAIN - pacientes cargados:", len(self.gestor.pacientes))

        except Exception:
            pass

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.ejecutar()