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
    
    def cantidad_total_correos(self):
        return len(self.recibidos) + len(self.enviados) 

    def cantidad_recibidos(self):
        return len(self.recibidos) 

    def cantidad_enviados(self):
        return len(self.enviados) 

    def cantidad_no_leidos(self):
        # Filtra los correos en la carpeta recibidos que tengan la propiedad leido en False
        return len([c for c in self.recibidos if not c.leido]) 

    def cantidad_contactos(self):
        return len(self.contactos)