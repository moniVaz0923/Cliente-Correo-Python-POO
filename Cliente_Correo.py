# --- Cliente_Correo.py (VERSIÓN LIMPIA PARA GITHUB) ---
from Connectar_bd import obtener_conexion

class Cuenta:
    def __init__(self, usuario, direccion, servidor_pop, servidor_smtp):
        self.usuario = usuario
        self.direccion = direccion
        self.servidor_pop = servidor_pop
        self.servidor_smtp = servidor_smtp

class Correo:
    def __init__(self, remitente, asunto, mensaje):
        self.remitente = remitente
        self.asunto = asunto
        self.mensaje = mensaje
        self.leido = False # Esto evita cualquier error si el sistema busca si está leído

class Contacto:
    def __init__(self, nombre,apellido, correo):
        self.nombre = nombre
        self.apellido = apellido    
        self.correo = correo

class ClienteCorreo:
    def __init__(self, cuenta):
        self.cuenta = cuenta
        # Dejamos las listas listas para usar, pero el guardado real 
        # lo hace la Ventana_Principal.py en el archivo JSON
        self.recibidos = []
        self.enviados = []
        self.contactos = [] 
        self.db = obtener_conexion() 
        # Al instanciar el objeto, cargamos lo que ya existe en MySQL a memoria para trabajar con objetos en la aplicación
        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        """Lee la base de datos y crea los objetos en memoria"""
        if self.db and self.db.is_connected():
            try:
                cursor = self.db.cursor(dictionary=True)
                
                # 1. Cargar Contactos
                cursor.execute("SELECT * FROM contactos")
                for fila in cursor.fetchall():
                    con = Contacto(fila['nombre'], fila['apellido'], fila['email'])
                    self.contactos.append(con)

                # 2. Cargar Correos (Recibidos y Enviados)
                cursor.execute("SELECT * FROM correos")
                for fila in cursor.fetchall():
                    # Convertimos el texto de la DB de nuevo a una lista de Python
                    dests = fila['destinatario'].split(", ")
                    correo = Correo(fila['asunto'], fila['mensaje'], fila['remitente'], dests, bool(fila['leido']))
                    
                    if fila['tipo'] == 'recibido':
                        self.recibidos.append(correo)
                    else:
                        self.enviados.append(correo)
                print("Datos cargados exitosamente desde MySQL.")
            except Exception as e:
                print(f"Error al cargar datos: {e}")

    def agregar_contacto_db(self, contacto):
        """Guarda un nuevo objeto Contacto en MySQL """
        if self.db and self.db.is_connected():
            try:
                cursor = self.db.cursor()
                sql = "INSERT INTO contactos (nombre, apellido, email) VALUES (%s, %s, %s)"
                cursor.execute(sql, (contacto.nombre, contacto.apellido, contacto.email))
                self.db.commit()
            except Exception as e:
                print(f"Error MySQL: {e}")
        self.contactos.append(contacto)

    def enviar_correo(self, unCorreo):
        """Guarda un objeto Correo en la carpeta 'enviados' de MySQL"""
        if self.db and self.db.is_connected():
            try:
                cursor = self.db.cursor()
                sql = "INSERT INTO correos (asunto, mensaje, remitente, destinatario, leido, tipo) VALUES (%s, %s, %s, %s, %s, %s)"
                dest_str = ", ".join(unCorreo.destinatario)
                cursor.execute(sql, (unCorreo.asunto, unCorreo.mensaje, unCorreo.remitente, dest_str, unCorreo.leido, 'enviado'))
                self.db.commit()
            except Exception as e:
                print(f"Error MySQL: {e}")
        self.enviados.append(unCorreo)

    # Métodos de conteo (Capacidades del objeto)
    def cantidad_total_correos(self):
        return len(self.recibidos) + len(self.enviados)

    def cantidad_recibidos(self):
        return len(self.recibidos)

    def cantidad_no_leidos(self):
        return len([c for c in self.recibidos if not c.leido])
    