import tkinter as tk
from tkinter import ttk, messagebox
from models.paciente import Paciente
from utils import validaciones as val
from styles import EstilosHospital

class VentanaRegistro:
    def __init__(self, parent, gestor, callback_actualizar):
        self.parent = parent
        self.gestor = gestor
        self.callback_actualizar = callback_actualizar
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Registrar Nuevo Paciente")
        self.ventana.geometry("650x750")
        self.ventana.resizable(False, False)
        self.ventana.configure(bg=EstilosHospital.COLORES["fondo"])
        
        self.entradas = {}
        self.crear_interfaz()
    
    def crear_interfaz(self):
        EstilosHospital.crear_header(self.ventana, "REGISTRO DE PACIENTE")
        
        frame = tk.Frame(self.ventana, bg=EstilosHospital.COLORES["fondo"], padx=30, pady=20)
        frame.pack(fill="both", expand=True)
        
        campos = [
            ("ID del Paciente:", "id", True),
            ("Nombre Completo:", "nombre", True),
            ("Tipo de Paciente:", "tipo", True),
            ("Hora de Llegada:", "llegada", True),
            ("Duracion de Atencion (min):", "rafaga", True),
            ("Prioridad (0-5):", "prioridad", False),
            ("Gestiones:", "gestiones", False)
        ]
        
        for i, (label, key, requerido) in enumerate(campos):
            lbl = tk.Label(
                frame,
                text=label,
                font=("Segoe UI", 10),
                bg=EstilosHospital.COLORES["fondo"],
                fg=EstilosHospital.COLORES["texto_oscuro"]
            )
            lbl.grid(row=i, column=0, padx=10, pady=8, sticky="e")
            
            if key == "tipo":
                tipos = ["Rojo", "Amarillo", "Embarazada", "Verde", "Cita", "Seguimiento"]
                entry = ttk.Combobox(frame, values=tipos, state="readonly", width=25)
                entry.set(tipos[0])
                entry.grid(row=i, column=1, padx=10, pady=8)
                self.entradas[key] = entry
            
            elif key == "llegada":
                frame_hora = tk.Frame(frame, bg=EstilosHospital.COLORES["fondo"])
                frame_hora.grid(row=i, column=1, padx=10, pady=8)
                
                horas = [f"{h:02d}" for h in range(24)]
                minutos = [f"{m:02d}" for m in range(0, 60, 5)]
                
                combo_hora = ttk.Combobox(frame_hora, values=horas, state="readonly", width=5)
                combo_hora.set("08")
                combo_hora.pack(side="left")
                
                tk.Label(frame_hora, text=":", font=("Segoe UI", 12), bg=EstilosHospital.COLORES["fondo"]).pack(side="left")
                
                combo_minuto = ttk.Combobox(frame_hora, values=minutos, state="readonly", width=5)
                combo_minuto.set("00")
                combo_minuto.pack(side="left")
                
                self.entradas["hora"] = combo_hora
                self.entradas["minuto"] = combo_minuto
            
            else:
                entry = tk.Entry(frame, width=27, font=("Segoe UI", 10))
                if requerido:
                    entry.config(bg="#FFF8E1")
                entry.grid(row=i, column=1, padx=10, pady=8)
                self.entradas[key] = entry
        
        info = tk.Label(
            frame,
            text="* Campos con fondo amarillo son obligatorios",
            font=("Segoe UI", 8),
            fg="#888888",
            bg=EstilosHospital.COLORES["fondo"]
        )
        info.grid(row=len(campos), column=0, columnspan=2, pady=10)
        
        btn_frame = tk.Frame(self.ventana, bg=EstilosHospital.COLORES["fondo"])
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame,
            text="Registrar Paciente",
            command=self.registrar,
            bg=EstilosHospital.COLORES["rojo_principal"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=30,
            pady=8,
            relief="raised",
            bd=2,
            activebackground=EstilosHospital.COLORES["rojo_hover"],
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
            pady=8,
            relief="raised",
            bd=2,
            activebackground=EstilosHospital.COLORES["gris_hover"],
            activeforeground="white",
            cursor="hand2"
        ).pack(side="left", padx=10)
    
    def registrar(self):
        try:
            id_val, msg = val.validar_id(self.entradas["id"].get())
            if not id_val:
                messagebox.showerror("Error de Validacion", f"ID: {msg}")
                return
            
            nombre = val.limpiar_campo(self.entradas["nombre"].get())
            if not nombre:
                messagebox.showerror("Error de Validacion", "El nombre es obligatorio")
                return
            
            tipo = self.entradas["tipo"].get()
            if tipo not in ["Rojo", "Amarillo", "Embarazada", "Verde", "Cita", "Seguimiento"]:
                messagebox.showerror("Error de Validacion", "Tipo de paciente no valido")
                return
            
            hora = int(self.entradas["hora"].get())
            minuto = int(self.entradas["minuto"].get())
            llegada = hora
            
            rafaga_val, msg = val.validar_rafaga(self.entradas["rafaga"].get())
            if not rafaga_val:
                messagebox.showerror("Error de Validacion", f"Duracion de atencion: {msg}")
                return
            
            prioridad = None
            if self.entradas["prioridad"].get():
                prioridad_val, msg = val.validar_prioridad(self.entradas["prioridad"].get())
                if not prioridad_val:
                    messagebox.showerror("Error de Validacion", f"Prioridad: {msg}")
                    return
                prioridad = int(self.entradas["prioridad"].get())
            
            gestiones = 1
            if self.entradas["gestiones"].get():
                gest_val, msg = val.validar_gestiones(self.entradas["gestiones"].get())
                if not gest_val:
                    messagebox.showerror("Error de Validacion", f"Gestiones: {msg}")
                    return
                gestiones = int(self.entradas["gestiones"].get())
            
            self.gestor.registrar_paciente(
                int(self.entradas["id"].get()),
                nombre,
                tipo,
                llegada,
                int(self.entradas["rafaga"].get()),
                prioridad,
                gestiones
            )
            
            self.gestor.guardar_en_txt("data/pacientes_registrados.txt")
            
            messagebox.showinfo(
                "Exito",
                "Paciente registrado correctamente.\nSe ha generado el tiquete de atencion.\nLos datos han sido guardados automaticamente."
            )
            self.ventana.destroy()
            self.callback_actualizar()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")