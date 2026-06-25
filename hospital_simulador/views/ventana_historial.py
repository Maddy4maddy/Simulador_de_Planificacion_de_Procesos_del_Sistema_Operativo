import tkinter as tk
from tkinter import ttk
from styles import EstilosHospital


class VentanaHistorial:

    def __init__(self, root, historial_controller):
         #Inicializa la ventana secundaria y establece la referencia
        #al controlador del historial para consultar la información almacenada.
        self.historial = historial_controller

        self.ventana = tk.Toplevel(root)
        self.ventana.title("Historial de Ejecuciones")
        self.ventana.geometry("1000x600")
        self.ventana.configure(bg=EstilosHospital.COLORES["fondo"])

        self.crear_ui()
        self.cargar_ejecuciones()

    def crear_ui(self):
        #Construye toda la interfaz gráfica de la ventana.
        EstilosHospital.crear_header(self.ventana, "HISTORIAL DE EJECUCIONES")

        frame_superior = tk.Frame(self.ventana, bg=EstilosHospital.COLORES["fondo"])
        frame_superior.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(
            frame_superior,
            text="Ejecuciones anteriores:",
            font=("Segoe UI", 10, "bold"),
            bg=EstilosHospital.COLORES["fondo"],
            fg=EstilosHospital.COLORES["texto_oscuro"]
        ).pack(anchor="w")

         #Tabla que muestra el resumen de todas las ejecuciones registradas.
        cols_ejec = ("ID Ejecución", "Fecha", "Algoritmo", "Pacientes",
                     "Prom. Espera", "Prom. Retorno", "CPU %")
        self.tree_ejec = ttk.Treeview(frame_superior, columns=cols_ejec, show="headings", height=7)

        anchos = [160, 160, 90, 80, 110, 110, 80]
        for col, ancho in zip(cols_ejec, anchos):
            self.tree_ejec.heading(col, text=col.upper())
            self.tree_ejec.column(col, width=ancho, anchor="center")

        scroll_ejec = ttk.Scrollbar(frame_superior, orient="vertical", command=self.tree_ejec.yview)
        self.tree_ejec.configure(yscrollcommand=scroll_ejec.set)
        self.tree_ejec.pack(side="left", fill="both", expand=True)
        scroll_ejec.pack(side="right", fill="y")

          #Evento que permite mostrar el detalle de una ejecución.
        self.tree_ejec.bind("<<TreeviewSelect>>", self.mostrar_detalle)

        frame_inferior = tk.Frame(self.ventana, bg=EstilosHospital.COLORES["fondo"])
        frame_inferior.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        tk.Label(
            frame_inferior,
            text="Pacientes de la ejecución seleccionada:",
            font=("Segoe UI", 10, "bold"),
            bg=EstilosHospital.COLORES["fondo"],
            fg=EstilosHospital.COLORES["texto_oscuro"]
        ).pack(anchor="w")

        # Tabla destinada a mostrar los pacientes pertenecientes a la ejecución seleccionada.
        cols_pac = ("ID", "Nombre", "Tipo", "Prioridad", "Gestiones",
                    "T. Espera", "T. Retorno")
        self.tree_pac = ttk.Treeview(frame_inferior, columns=cols_pac, show="headings", height=7)

        anchos_pac = [60, 180, 110, 80, 80, 90, 90]
        for col, ancho in zip(cols_pac, anchos_pac):
            self.tree_pac.heading(col, text=col.upper())
            self.tree_pac.column(col, width=ancho, anchor="center")

        scroll_pac = ttk.Scrollbar(frame_inferior, orient="vertical", command=self.tree_pac.yview)
        self.tree_pac.configure(yscrollcommand=scroll_pac.set)
        self.tree_pac.pack(side="left", fill="both", expand=True)
        scroll_pac.pack(side="right", fill="y")

        #Botón que permite cerrar la ventana del historial.
        btn_frame = tk.Frame(self.ventana, bg=EstilosHospital.COLORES["fondo"])
        btn_frame.pack(pady=8)

        tk.Button(
            btn_frame,
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
        ).pack()

    def cargar_ejecuciones(self):
        #Limpia la tabla de ejecuciones y carga nuevamente todos los registros almacenados en el historial.
        for item in self.tree_ejec.get_children():
            self.tree_ejec.delete(item)

        for e in self.historial.obtener_ejecuciones():
            self.tree_ejec.insert("", "end", iid=e["ejecucion_id"], values=(
                e["ejecucion_id"],
                e["fecha"],
                e["algoritmo"],
                e["total_pacientes"],
                e["prom_espera"],
                e["prom_retorno"],
                e["cpu_utilizacion"]
            ))

    def mostrar_detalle(self, event):
        #Obtiene la ejecución seleccionada y muestra en la tabla inferior todos los pacientes asociados.
        seleccion = self.tree_ejec.selection()
        if not seleccion:
            return

        ejecucion_id = seleccion[0]

        for item in self.tree_pac.get_children():
            self.tree_pac.delete(item)

        for p in self.historial.obtener_pacientes_de_ejecucion(ejecucion_id):
            self.tree_pac.insert("", "end", values=(
                p["id_paciente"],
                p["nombre"],
                p["tipo"],
                p["prioridad"],
                p["gestiones"],
                p["tiempo_espera"],
                p["tiempo_retorno"]
            ))