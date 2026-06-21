import tkinter as tk
from tkinter import messagebox
from utils import validaciones as val
from styles import EstilosHospital

class VentanaEliminar:
    def __init__(self, parent, gestor, callback_actualizar):
        self.parent = parent
        self.gestor = gestor
        self.callback_actualizar = callback_actualizar
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Eliminar Paciente")
        self.ventana.geometry("450x200")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg=EstilosHospital.COLORES["fondo"])
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        EstilosHospital.crear_header(self.ventana, "ELIMINAR PACIENTE", EstilosHospital.COLORES["rojo_claro"])
        
        frame = tk.Frame(self.ventana, bg=EstilosHospital.COLORES["fondo"], pady=30)
        frame.pack(fill="both", expand=True)
        
        tk.Label(
            frame,
            text="ID del paciente a eliminar:",
            font=("Segoe UI", 10),
            bg=EstilosHospital.COLORES["fondo"],
            fg=EstilosHospital.COLORES["texto_oscuro"]
        ).pack(side="left", padx=10)
        
        self.entry_id = tk.Entry(frame, width=15, font=("Segoe UI", 10))
        self.entry_id.pack(side="left", padx=10)
        
        btn_frame = tk.Frame(self.ventana, bg=EstilosHospital.COLORES["fondo"])
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="Eliminar",
            command=self.eliminar,
            bg=EstilosHospital.COLORES["rojo_claro"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=25,
            pady=6,
            relief="raised",
            bd=2,
            activebackground=EstilosHospital.COLORES["rojo_hover_claro"],
            activeforeground="white",
            cursor="hand2"
        ).pack(side="left", padx=10)
        
        tk.Button(
            btn_frame,
            text="Cancelar",
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
        ).pack(side="left", padx=10)
    
    def eliminar(self):
        try:
            id_val, msg = val.validar_id(self.entry_id.get())
            if not id_val:
                messagebox.showerror("Error", msg)
                return
            
            id_p = int(self.entry_id.get())
            paciente = self.gestor.buscar_por_id(id_p)
            
            if paciente:
                if messagebox.askyesno(
                    "Confirmar",
                    f"Esta seguro de eliminar al paciente:\n\nID: {id_p}\nNombre: {paciente.nombre}\nTipo: {paciente.tipo}"
                ):
                    if self.gestor.eliminar_paciente(id_p):
                        self.gestor.guardar_en_txt("data/pacientes_registrados.txt")
                        messagebox.showinfo("Exito", "Paciente eliminado correctamente.\nLos cambios han sido guardados.")
                        self.ventana.destroy()
                        self.callback_actualizar()
            else:
                messagebox.showerror("Error", f"No se encontro paciente con ID {id_p}")
                
        except Exception as e:
            messagebox.showerror("Error", str(e))