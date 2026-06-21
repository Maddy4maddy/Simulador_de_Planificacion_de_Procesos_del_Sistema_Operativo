import os
from models.paciente import Paciente
from models.tiquete import Tiquete

class GestorPacientes:
    
    def __init__(self):
        self.pacientes = []
        self.tiquetes = []
        self.id_set = set()
        self.ruta_archivo = "data/pacientes_registrados.txt"

    def registrar_paciente(self, id_paciente, nombre, tipo, tiempo_llegada, rafaga, prioridad=None, gestiones=1):
        if id_paciente in self.id_set:
            raise ValueError(f"El ID {id_paciente} ya existe en el sistema.")
        
        if tiempo_llegada < 0:
            raise ValueError("El tiempo de llegada no puede ser negativo.")
        
        if rafaga <= 0:
            raise ValueError("La rafaga debe ser mayor a 0.")
        
        if gestiones < 1:
            raise ValueError("Las gestiones deben ser al menos 1.")
        
        paciente = Paciente(id_paciente, nombre, tipo, tiempo_llegada, rafaga, prioridad, gestiones)
        self.pacientes.append(paciente)
        self.id_set.add(id_paciente)
        
        tiquete = Tiquete(paciente)
        self.tiquetes.append(tiquete)
        
        return paciente

    def eliminar_paciente(self, id_paciente):
        for p in self.pacientes:
            if p.id == id_paciente:
                self.pacientes.remove(p)
                self.id_set.remove(id_paciente)
                self.tiquetes = [t for t in self.tiquetes if t.paciente.id != id_paciente]
                return True
        return False

    def cargar_desde_txt(self, ruta=None):
        if ruta is None:
            ruta = self.ruta_archivo
            
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
        
        pacientes_cargados = 0
        errores = []
        
        with open(ruta, 'r', encoding='utf-8') as file:
            for num_linea, linea in enumerate(file, 1):
                linea = linea.strip()
                if not linea or linea.startswith('#'):
                    continue
                    
                try:
                    datos = linea.split(',')
                    if len(datos) < 6:
                        errores.append(f"Linea {num_linea}: Formato incorrecto")
                        continue
                    
                    id_p = int(datos[0].strip())
                    nombre = datos[1].strip()
                    tipo = datos[2].strip()
                    llegada = int(datos[3].strip())
                    rafaga = int(datos[4].strip())
                    prioridad = int(datos[5].strip()) if datos[5].strip() else None
                    gestiones = int(datos[6].strip()) if len(datos) > 6 and datos[6].strip() else 1
                    
                    if tipo not in Paciente.TIPOS_PRIORIDAD:
                        errores.append(f"Linea {num_linea}: Tipo '{tipo}' no valido")
                        continue
                    
                    self.registrar_paciente(id_p, nombre, tipo, llegada, rafaga, prioridad, gestiones)
                    pacientes_cargados += 1
                    
                except ValueError as e:
                    errores.append(f"Linea {num_linea}: {str(e)}")
                except Exception as e:
                    errores.append(f"Linea {num_linea}: Error inesperado - {str(e)}")
        
        if errores:
            raise ValueError(f"Se cargaron {pacientes_cargados} pacientes con {len(errores)} errores:\n" + "\n".join(errores[:5]))
        
        return pacientes_cargados

    def guardar_en_txt(self, ruta=None):
        if ruta is None:
            ruta = self.ruta_archivo
            
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        
        with open(ruta, 'w', encoding='utf-8') as file:
            file.write("# ID,Nombre,Tipo,Llegada,Rafaga,Prioridad,Gestiones\n")
            for p in self.pacientes:
                file.write(f"{p.id},{p.nombre},{p.tipo},{p.tiempo_llegada},{p.rafaga},{p.prioridad},{p.gestiones}\n")

    def listar_pacientes(self):
        return self.pacientes

    def buscar_por_id(self, id_paciente):
        for p in self.pacientes:
            if p.id == id_paciente:
                return p
        return None

    def obtener_tiquetes(self):
        return self.tiquetes

    def obtener_tiquete_por_paciente(self, id_paciente):
        for t in self.tiquetes:
            if t.paciente.id == id_paciente:
                return t
        return None

    def limpiar_sistema(self):
        self.pacientes.clear()
        self.tiquetes.clear()
        self.id_set.clear()
        Tiquete.contador = 1

    def contar_pacientes(self):
        return len(self.pacientes)