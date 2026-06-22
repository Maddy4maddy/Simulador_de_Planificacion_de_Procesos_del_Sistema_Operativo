import tkinter as tk
from tkinter import ttk


class EstilosHospital:

    COLORES = {
        "rojo_principal": "#8B0000",
        "rojo_oscuro": "#6B0000",
        "rojo_claro": "#CC0000",
        "rojo_hover": "#A52A2A",
        "rojo_hover_claro": "#DD2222",

        "fondo": "#FDF2F2",
        "fondo_claro": "#FFF5F5",

        "texto_oscuro": "#4A0000",
        "blanco": "#FFFFFF",

        "gris": "#555555",
        "gris_hover": "#777777",

        "naranja": "#E65100",
        "verde": "#2E7D32",

        # estados simulación
        "estado_espera": "#FFF3E0",
        "estado_atencion": "#FFCDD2",
        "estado_finalizado": "#C8E6C9",

        # Gantt
        "gantt_barra": "#8B0000",
        "gantt_texto": "#FFFFFF"
    }

    TIPOS_PACIENTE = {
        "Rojo": {"bg": "#FF0000", "fg": "white", "prioridad": 5},
        "Amarillo": {"bg": "#FFD700", "fg": "black", "prioridad": 4},
        "Embarazada": {"bg": "#FF69B4", "fg": "black", "prioridad": 3},
        "Verde": {"bg": "#00FF00", "fg": "black", "prioridad": 2},
        "Cita": {"bg": "#4169E1", "fg": "white", "prioridad": 1},
        "Seguimiento": {"bg": "#808080", "fg": "white", "prioridad": 0}
    }

    # -------------------------
    # ESTILOS TTK
    # -------------------------
    @classmethod
    def aplicar_estilos_ttk(cls):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground=cls.COLORES["rojo_principal"]
        )

        style.configure(
            "Header.TLabel",
            font=("Segoe UI", 12, "bold"),
            foreground=cls.COLORES["rojo_oscuro"]
        )

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=28
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background=cls.COLORES["rojo_principal"],
            foreground="white"
        )

        style.map(
            "Treeview.Heading",
            background=[("active", cls.COLORES["rojo_hover"])]
        )

        style.configure(
            "TLabelframe",
            background=cls.COLORES["fondo"],
            foreground=cls.COLORES["rojo_principal"]
        )

        style.configure(
            "TLabelframe.Label",
            font=("Segoe UI", 11, "bold"),
            foreground=cls.COLORES["rojo_principal"]
        )

    # -------------------------
    # BOTONES
    # -------------------------
    @classmethod
    def crear_boton_rojo(cls, parent, texto, comando):
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=cls.COLORES["rojo_principal"],
            fg=cls.COLORES["blanco"],
            font=("Segoe UI", 9, "bold"),
            padx=15,
            pady=8,
            relief="raised",
            bd=2,
            activebackground=cls.COLORES["rojo_hover"],
            activeforeground=cls.COLORES["blanco"],
            cursor="hand2"
        )

    @classmethod
    def crear_boton_eliminar(cls, parent, texto, comando):
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=cls.COLORES["rojo_claro"],
            fg=cls.COLORES["blanco"],
            font=("Segoe UI", 9, "bold"),
            padx=15,
            pady=8,
            relief="raised",
            bd=2,
            activebackground=cls.COLORES["rojo_hover_claro"],
            activeforeground=cls.COLORES["blanco"],
            cursor="hand2"
        )

    @classmethod
    def crear_boton_gris(cls, parent, texto, comando):
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=cls.COLORES["gris"],
            fg=cls.COLORES["blanco"],
            font=("Segoe UI", 9),
            padx=15,
            pady=8,
            relief="raised",
            bd=2,
            activebackground=cls.COLORES["gris_hover"],
            activeforeground=cls.COLORES["blanco"],
            cursor="hand2"
        )

    # -------------------------
    # HEADER
    # -------------------------
    @classmethod
    def crear_header(cls, parent, texto, color=None):
        color = color or cls.COLORES["rojo_principal"]

        frame = tk.Frame(parent, bg=color, height=60)
        frame.pack(fill="x")
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=texto,
            font=("Segoe UI", 16, "bold"),
            fg=cls.COLORES["blanco"],
            bg=color
        ).pack(expand=True)

        return frame

    # -------------------------
    # BARRA SUPERIOR
    # -------------------------
    @classmethod
    def crear_barra_superior(cls, parent):
        frame = tk.Frame(parent, bg=cls.COLORES["rojo_principal"], height=80)
        frame.pack(fill="x", side="top")
        frame.pack_propagate(False)

        container = tk.Frame(frame, bg=cls.COLORES["rojo_principal"])
        container.pack(expand=True, fill="both", padx=20)

        tk.Label(
            container,
            text="HOSPITAL CENTRO DE EMERGENCIAS",
            font=("Segoe UI", 20, "bold"),
            fg=cls.COLORES["blanco"],
            bg=cls.COLORES["rojo_principal"]
        ).pack(side="left")

        tk.Label(
            container,
            text="Sistema de Gestión de Pacientes y Tiquetes",
            font=("Segoe UI", 11),
            fg="#FFD7D7",
            bg=cls.COLORES["rojo_principal"]
        ).pack(side="left", padx=20)

        return frame