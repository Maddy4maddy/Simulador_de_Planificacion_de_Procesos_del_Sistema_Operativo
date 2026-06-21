import tkinter as tk
from controllers.gestor_pacientes import GestorPacientes
from views import VentanaPrincipal
import os

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestion Hospitalaria - Centro de Emergencias")
        self.root.geometry("1200x750")
        self.root.resizable(True, True)
        
        self.gestor = GestorPacientes()
        self.archivo_actual = "data/pacientes_registrados.txt"
        
        self.cargar_archivo_inicio()
        
        self.ventana_principal = VentanaPrincipal(
            self.root,
            self.gestor,
            self.archivo_actual
        )
        
        self.ventana_principal.actualizar_lista()
    
    def cargar_archivo_inicio(self):
        try:
            if os.path.exists(self.archivo_actual):
                self.gestor.cargar_desde_txt(self.archivo_actual)
        except Exception as e:
            pass
    
    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.ejecutar()