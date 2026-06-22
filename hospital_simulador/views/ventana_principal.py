import tkinter as tk
from tkinter import ttk, messagebox
from views.ventana_registro import VentanaRegistro
from views.ventana_eliminar import VentanaEliminar
from views.ventana_tiquetes import VentanaTiquetes
from views.ventana_metricas import VentanaMetricas
from views.ventana_comparacion import VentanaComparacion
from controllers.simulation_step_controller import SimulationStepController
from views.ventana_simulacion_paso import VentanaSimulacionPaso

from views.ventana_gantt import VentanaGantt
from styles import EstilosHospital

class VentanaPrincipal:
    def __init__(self, root, gestor, archivo_actual, simulation, comparador):
        self.root = root
        self.gestor = gestor
        self.archivo_actual = archivo_actual
        self.simulation = simulation
        self.comparador = comparador
        self.tree = None
        self.status_bar = None
        self.lbl_total = None
        self.lbl_espera = None
        self.lbl_atencion = None
        self.lbl_finalizados = None
        
        self.config_mlq_vars = {
        "Rojo": tk.StringVar(value="FIFO"),
        "Amarillo": tk.StringVar(value="SJF"),
        "Embarazada": tk.StringVar(value="RR"),
        "Verde": tk.StringVar(value="FIFO"),
        "Cita": tk.StringVar(value="SJF"),
        "Seguimiento": tk.StringVar(value="RR")
        }

        self.crear_interfaz()
    
    def crear_interfaz(self):
        self.crear_menu_principal()
        self.crear_lista_pacientes()
        self.crear_panel_estadisticas()
        self.crear_barra_estado()
            
        
    def crear_menu_principal(self):

        menu_frame = tk.LabelFrame(
            self.root,
            text="Panel de Control",
            font=("Segoe UI", 11, "bold"),
            fg=EstilosHospital.COLORES["rojo_principal"],
            bg=EstilosHospital.COLORES["fondo"],
            padx=10,
            pady=10
        )
        menu_frame.pack(fill="x", padx=10, pady=5)

        canvas = tk.Canvas(
            menu_frame,
            height=300,
            bg=EstilosHospital.COLORES["fondo"],
            highlightthickness=0
        )
        canvas.pack(fill="x", expand=True)

        scrollbar_x = tk.Scrollbar(
            menu_frame,
            orient="horizontal",
            command=canvas.xview
        )
        scrollbar_x.pack(fill="x")

        canvas.configure(
            xscrollcommand=scrollbar_x.set
        )

        scroll_frame = tk.Frame(
            canvas,
            bg=EstilosHospital.COLORES["fondo"]
        )

        window = canvas.create_window(
            (0, 0),
            window=scroll_frame,
            anchor="nw"
        )

        def _on_configure(event):
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        scroll_frame.bind("<Configure>", _on_configure)

        self.crear_config_mlq(scroll_frame)

        separador = tk.Frame(
            scroll_frame,
            height=10,
            bg=EstilosHospital.COLORES["fondo"]
        )
        separador.pack(fill="x")

        botones_frame = tk.Frame(
            scroll_frame,
            bg=EstilosHospital.COLORES["fondo"]
        )
        botones_frame.pack(fill="x", pady=5)

        botones = [
            ("Registrar Paciente", self.abrir_registro),
            ("Cargar desde TXT", self.cargar_txt),
            ("Guardar en TXT", self.guardar_txt),
            ("Eliminar Paciente", self.abrir_eliminar),
            ("Actualizar Lista", self.actualizar_lista),
            ("Ver Tiquetes", self.abrir_tiquetes),
            ("Simulación MLQ", self.ejecutar_mlq),
            ("Comparar Algoritmos", self.abrir_comparacion),
            ("Ver Gantt", self.abrir_gantt),
            ("Simulación Paso a Paso", self.abrir_simulacion_paso),
            ("Limpiar Sistema", self.limpiar_sistema),
            ("Salir", self.root.quit)
        ]

        for texto, comando in botones:

            if "Eliminar" in texto or "Limpiar" in texto:
                btn = EstilosHospital.crear_boton_eliminar(
                    botones_frame,
                    texto,
                    comando
                )

            elif "Salir" in texto:
                btn = EstilosHospital.crear_boton_gris(
                    botones_frame,
                    texto,
                    comando
                )

            else:
                btn = EstilosHospital.crear_boton_rojo(
                    botones_frame,
                    texto,
                    comando
                )

            btn.pack(
                side="left",
                padx=4,
                pady=5
            )

        canvas.update_idletasks()

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    def crear_lista_pacientes(self):
        list_frame = tk.LabelFrame(
            self.root,
            text="Pacientes Registrados",
            font=("Segoe UI", 11, "bold"),
            fg=EstilosHospital.COLORES["rojo_principal"],
            bg=EstilosHospital.COLORES["fondo"],
            padx=10,
            pady=10
        )
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        table_frame = tk.Frame(list_frame, bg=EstilosHospital.COLORES["fondo"])
        table_frame.pack(fill="both", expand=True)
        
        columnas = ("ID", "Nombre", "Tipo", "Prioridad", "Llegada", "Rafaga",
                   "Restante", "Gestiones", "Tiquete", "Estado")
        
        self.tree = ttk.Treeview(table_frame, columns=columnas, show="headings", height=8)
        
        anchos = [60, 180, 120, 80, 80, 100, 100, 80, 100, 120]
        for col, ancho in zip(columnas, anchos):
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=ancho, anchor="center")
        
        scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        self.tree.tag_configure("espera", background=EstilosHospital.COLORES["estado_espera"])
        self.tree.tag_configure("atencion", background=EstilosHospital.COLORES["estado_atencion"])
        self.tree.tag_configure("finalizado", background=EstilosHospital.COLORES["estado_finalizado"])
    
    def crear_panel_estadisticas(self):
        stats_frame = tk.Frame(self.root, bg=EstilosHospital.COLORES["fondo"], height=60)
        stats_frame.pack(fill="x", padx=10, pady=5)
        stats_frame.pack_propagate(False)
        
        container = tk.Frame(stats_frame, bg=EstilosHospital.COLORES["fondo"])
        container.pack(fill="both", expand=True)
        
        self.lbl_total = tk.Label(
            container,
            text="Total: 0",
            font=("Segoe UI", 11, "bold"),
            fg=EstilosHospital.COLORES["rojo_principal"],
            bg=EstilosHospital.COLORES["fondo"]
        )
        self.lbl_total.pack(side="left", padx=20)
        
        self.lbl_espera = tk.Label(
            container,
            text="En Espera: 0",
            font=("Segoe UI", 11),
            fg=EstilosHospital.COLORES["naranja"],
            bg=EstilosHospital.COLORES["fondo"]
        )
        self.lbl_espera.pack(side="left", padx=20)
        
        self.lbl_atencion = tk.Label(
            container,
            text="En Atencion: 0",
            font=("Segoe UI", 11),
            fg=EstilosHospital.COLORES["rojo_claro"],
            bg=EstilosHospital.COLORES["fondo"]
        )
        self.lbl_atencion.pack(side="left", padx=20)
        
        self.lbl_finalizados = tk.Label(
            container,
            text="Finalizados: 0",
            font=("Segoe UI", 11),
            fg=EstilosHospital.COLORES["verde"],
            bg=EstilosHospital.COLORES["fondo"]
        )
        self.lbl_finalizados.pack(side="left", padx=20)
        
        leyenda_frame = tk.Frame(container, bg=EstilosHospital.COLORES["fondo"])
        leyenda_frame.pack(side="right", padx=20)
        
        for tipo, datos in EstilosHospital.TIPOS_PACIENTE.items():
            lbl = tk.Label(
                leyenda_frame,
                text=tipo,
                bg=datos["bg"],
                fg=datos["fg"],
                padx=8,
                pady=2,
                font=("Segoe UI", 8, "bold"),
                relief="ridge",
                bd=1
            )
            lbl.pack(side="left", padx=2)
    
    def crear_barra_estado(self):
        self.status_bar = tk.Label(
            self.root,
            text="Sistema listo",
            relief="sunken",
            anchor="w",
            padx=15,
            bg=EstilosHospital.COLORES["fondo_claro"],
            fg=EstilosHospital.COLORES["texto_oscuro"],
            font=("Segoe UI", 9)
        )
        self.status_bar.pack(side="bottom", fill="x")
    
    def formatear_tiempo(self, minutos):
        if minutos < 60:
            return f"{minutos} min"
        elif minutos == 60:
            return "1 h"
        else:
            horas = minutos // 60
            resto = minutos % 60
            if resto == 0:
                return f"{horas} h"
            else:
                return f"{horas}h {resto}min"
    
    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for p in self.gestor.listar_pacientes():
            tiquete_num = f"#{p.tiquete.numero:04d}" if p.tiquete else "Sin tiquete"
            estado = p.estado
            
            tags = ()
            if estado == "Espera":
                tags = ("espera",)
            elif estado == "Atencion":
                tags = ("atencion",)
            elif estado == "Finalizado":
                tags = ("finalizado",)
            
            prioridad_texto = ""
            if p.prioridad >= 4:
                prioridad_texto = "Alta"
            elif p.prioridad >= 2:
                prioridad_texto = "Media"
            else:
                prioridad_texto = "Baja"
            
            self.tree.insert("", "end", values=(
                p.id,
                p.nombre,
                p.tipo,
                f"{p.prioridad} ({prioridad_texto})",
                f"{p.tiempo_llegada}:00",
                self.formatear_tiempo(p.rafaga),
                self.formatear_tiempo(p.tiempo_restante),
                p.gestiones,
                tiquete_num,
                estado
            ), tags=tags)
        
        self.actualizar_estadisticas()
    
    def actualizar_estadisticas(self):
        total = self.gestor.contar_pacientes()
        en_espera = sum(1 for p in self.gestor.pacientes if p.estado == "Espera")
        en_atencion = sum(1 for p in self.gestor.pacientes if p.estado == "Atencion")
        finalizados = sum(1 for p in self.gestor.pacientes if p.estado == "Finalizado")
        
        self.lbl_total.config(text=f"Total: {total}")
        self.lbl_espera.config(text=f"En Espera: {en_espera}")
        self.lbl_atencion.config(text=f"En Atencion: {en_atencion}")
        self.lbl_finalizados.config(text=f"Finalizados: {finalizados}")
        self.status_bar.config(text=f"Lista actualizada - {total} pacientes registrados")
    
    def abrir_registro(self):
        ventana = VentanaRegistro(self.root, self.gestor, self.actualizar_lista)
    
    def abrir_eliminar(self):
        ventana = VentanaEliminar(self.root, self.gestor, self.actualizar_lista)
    
    def abrir_tiquetes(self):
        ventana = VentanaTiquetes(self.root, self.gestor)
    
    def cargar_txt(self):
        from tkinter import filedialog, messagebox
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de pacientes",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if ruta:
            try:
                cargados = self.gestor.cargar_desde_txt(ruta)
                self.archivo_actual = ruta
                messagebox.showinfo("Exito", f"Se cargaron {cargados} pacientes correctamente.")
                self.actualizar_lista()
                self.status_bar.config(text=f"Archivo cargado: {ruta}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def guardar_txt(self):
        from tkinter import filedialog, messagebox
        ruta = filedialog.asksaveasfilename(
            title="Guardar pacientes en archivo",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if ruta:
            try:
                self.gestor.guardar_en_txt(ruta)
                self.archivo_actual = ruta
                messagebox.showinfo("Exito", "Pacientes guardados correctamente.")
                self.status_bar.config(text=f"Archivo guardado: {ruta}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def limpiar_sistema(self):
        from tkinter import messagebox
        if messagebox.askyesno(
            "Confirmar",
            "Esta seguro de eliminar TODOS los pacientes del sistema?\n\nEsta accion no se puede deshacer."
        ):
            self.gestor.limpiar_sistema()
            self.gestor.guardar_en_txt(self.archivo_actual)
            self.actualizar_lista()
            messagebox.showinfo("Exito", "Sistema limpiado correctamente.\nLos cambios han sido guardados.")
            self.status_bar.config(text="Sistema limpiado - Todos los pacientes eliminados")


    def ejecutar_mlq(self):

        configuracion = {
            cola: var.get()
            for cola, var in self.config_mlq_vars.items()
        }

        resultado = self.simulation.ejecutar(
            configuracion,
            quantum=2
        )

        if not resultado or "error" in resultado:
            messagebox.showerror("Error", resultado["error"])
            return

        self.abrir_gantt(resultado)
        self.abrir_metricas(resultado)

        messagebox.showinfo(
            "MLQ Ejecutado",
            f"Pacientes procesados: {len(resultado['pacientes'])}\n"
            f"Configuración dinámica aplicada"
        )


    def comparar_algoritmos(self):

        resultado = self.root.master.comparador.ejecutar_comparacion(
        self.gestor.listar_pacientes(),
        quantum=2
        )

        resumen = resultado["comparacion"]

        mensaje = "COMPARACIÓN DE ALGORITMOS\n\n"

        for alg, data in resumen.items():

            mensaje += f"=== {alg} ===\n"
            mensaje += f"Espera promedio: {data['promedio_espera']:.2f}\n"
            mensaje += f"Retorno promedio: {data['promedio_retorno']:.2f}\n"
            mensaje += f"CPU: {data['cpu_utilizacion']:.2f}%\n"
            mensaje += f"Tiempo total: {data['tiempo_total']}\n\n"
        

        messagebox.showinfo("Comparación de Algoritmos", mensaje)

    def abrir_gantt(self, resultado=None):

        # si no viene resultado, ejecuta MLQ
        if resultado is None:
            resultado = self.simulation.ejecutar(
                configuracion={
                    "Rojo": "FIFO",
                    "Amarillo": "SJF",
                    "Embarazada": "RR",
                    "Verde": "FIFO",
                    "Cita": "SJF",
                    "Seguimiento": "RR"
                },
                quantum=2
            )

        if not resultado or "error" in resultado:
            messagebox.showerror("Error", "No hay datos para Gantt")
            return

        VentanaGantt(self.root, resultado["gantt"])

    def abrir_metricas(self, resultado):

        if not resultado or "metricas" not in resultado:
            print("No hay métricas disponibles")
            return

        VentanaMetricas(self.root, resultado["metricas"])

    def abrir_comparacion(self):

        pacientes = self.gestor.listar_pacientes()

        if not pacientes:
            print("No hay pacientes")
            return

        resultado = self.comparador.ejecutar_comparacion(pacientes)

        VentanaComparacion(self.root, resultado)

    def abrir_simulacion_paso(self):

        controller = SimulationStepController(self.gestor)

        VentanaSimulacionPaso(self.root, controller)

    def crear_config_mlq(self, parent):

        frame = tk.LabelFrame(
            parent,
            text="Configuración MLQ",
            bg=EstilosHospital.COLORES["fondo"]
        )
        frame.pack(fill="x", padx=10, pady=5)

        opciones = ["FIFO", "SJF", "RR"]

        for cola, var in self.config_mlq_vars.items():

            fila = tk.Frame(frame, bg=EstilosHospital.COLORES["fondo"])
            fila.pack(side="top", anchor="w", padx=10, pady=2)

            tk.Label(
                fila,
                text=cola,
                bg=EstilosHospital.COLORES["fondo"]
            ).pack(side="left")

            combo = ttk.Combobox(
                fila,
                textvariable=var,
                values=opciones,
                state="readonly",
                width=8
            )
            combo.pack(side="left", padx=5)