import tkinter as tk
from tkinter import ttk
from styles import EstilosHospital

class VentanaTiquetes:
    def __init__(self, parent, gestor):
        self.parent = parent
        self.gestor = gestor
        
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Tiquetes de Atencion")
        self.ventana.geometry("800x450")
        self.ventana.configure(bg=EstilosHospital.COLORES["fondo"])
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        EstilosHospital.crear_header(self.ventana, "TIQUETES DE ATENCION EMITIDOS", EstilosHospital.COLORES["rojo_oscuro"])
        
        if not self.gestor.tiquetes:
            tk.Label(
                self.ventana,
                text="No hay tiquetes emitidos en el sistema",
                font=("Segoe UI", 12),
                fg="#888888",
                bg=EstilosHospital.COLORES["fondo"]
            ).pack(expand=True)
        else:
            frame = tk.Frame(self.ventana, bg=EstilosHospital.COLORES["fondo"], padx=20, pady=20)
            frame.pack(fill="both", expand=True)
            
            columnas = ("Tiquete", "Paciente", "Tipo", "Prioridad", "Estado", "Fecha Emision")
            tree = ttk.Treeview(frame, columns=columnas, show="headings", height=15)
            
            anchos = [100, 180, 120, 80, 120, 180]
            for col, ancho in zip(columnas, anchos):
                tree.heading(col, text=col.upper())
                tree.column(col, width=ancho, anchor="center")
            
            scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scroll.set)
            
            tree.pack(side="left", fill="both", expand=True)
            scroll.pack(side="right", fill="y")
            
            for t in self.gestor.tiquetes:
                tree.insert("", "end", values=(
                    f"#{t.numero:04d}",
                    t.paciente.nombre,
                    t.paciente.tipo,
                    t.paciente.prioridad,
                    t.estado,
                    t.fecha_emision
                ))
        
        btn_cerrar = tk.Button(
            self.ventana,
            text="Cerrar",
            command=self.ventana.destroy,
            bg=EstilosHospital.COLORES["rojo_oscuro"],
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=30,
            pady=8,
            relief="raised",
            bd=2,
            activebackground=EstilosHospital.COLORES["rojo_principal"],
            activeforeground="white",
            cursor="hand2"
        )
        btn_cerrar.pack(pady=15)