# --- Cliente_Correo.py (VERSIÓN LIMPIA PARA GITHUB) ---

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

    # Dejamos estas funciones por si algún otro archivo intentara llamarlas, 
    # pero usamos "pass" para que no hagan nada ni tiren errores.
    def conectar(self):
        pass

    def descargar_correos(self):
        pass
        
    def enviar_correo(self, correo):
        pass