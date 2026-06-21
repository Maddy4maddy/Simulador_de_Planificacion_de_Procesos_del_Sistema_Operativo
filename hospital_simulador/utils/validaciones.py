import re

def validar_id(id_str):
    try:
        id_num = int(id_str)
        return id_num > 0, "El ID debe ser un numero positivo"
    except ValueError:
        return False, "El ID debe ser un numero entero"

def validar_nombre(nombre):
    if not nombre or not nombre.strip():
        return False, "El nombre no puede estar vacio"
    if len(nombre.strip()) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    return True, ""

def validar_tiempo(tiempo_str):
    try:
        tiempo = int(tiempo_str)
        return tiempo >= 0, "El tiempo no puede ser negativo"
    except ValueError:
        return False, "Debe ingresar un numero entero"

def validar_rafaga(rafaga_str):
    try:
        rafaga = int(rafaga_str)
        return rafaga > 0, "La rafaga debe ser mayor a 0"
    except ValueError:
        return False, "Debe ingresar un numero entero"

def validar_gestiones(gestiones_str):
    try:
        gestiones = int(gestiones_str)
        return gestiones >= 1, "Las gestiones deben ser al menos 1"
    except ValueError:
        return False, "Debe ingresar un numero entero"

def validar_prioridad(prioridad_str):
    try:
        prioridad = int(prioridad_str)
        return 0 <= prioridad <= 5, "La prioridad debe estar entre 0 y 5"
    except ValueError:
        return False, "Debe ingresar un numero entero"

def validar_tipo(tipo):
    tipos_validos = ["Rojo", "Amarillo", "Embarazada", "Verde", "Cita", "Seguimiento"]
    return tipo in tipos_validos, f"Tipo debe ser uno de: {', '.join(tipos_validos)}"

def limpiar_campo(valor):
    return valor.strip() if valor else ""