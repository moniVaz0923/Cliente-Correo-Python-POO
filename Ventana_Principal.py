import tkinter as tk
from Connectar_bd import obtener_conexion 
from tkinter import messagebox, ttk 
from Cliente_Correo import ClienteCorreo, Cuenta, Correo, Contacto

class AppCorreo:
    def __init__(self, root, cliente):
        self.cliente = cliente
        self.root = root
        self.root.title(f"UNSADA Mail - {self.cliente.cuenta.usuario}")
        self.root.geometry("700x500") 
        self.root.configure(bg="#f5f6f7") 

# --- 1. Variables de Interfaz (IMPORTANTE para que no de AttributeError) ---
        self.resumen_text = tk.StringVar()
        self.resumen_text.set(self.obtener_resumen())

        # --- 1. Encabezado ---
        self.header = tk.Frame(root, bg="#14b685", height=50) 
        self.header.pack(fill="x")
        
        tk.Label(self.header, text="UNSADA Mail", bg="#14b685", fg="white", 
                 font=("Segoe UI", 14, "bold")).pack(pady=10, padx=20, side="left")

        # --- 2. Barra de Herramientas (Botones arriba) ---
        self.toolbar = tk.Frame(root, bg="white", bd=1, relief="raised")
        self.toolbar.pack(fill="x")

        style = ttk.Style()
        style.configure("Tool.TButton", font=("Segoe UI", 9), padding=5)
        
        # --- 3. Panel de Resumen---
        self.info_frame = tk.LabelFrame(root, text=" Resumen de Actividad ", padx=20, pady=20, bg="white", font=("Segoe UI", 10, "bold"))
        self.info_frame.pack(pady=30, padx=30, fill="both", expand=True)

        self.lbl_resumen = tk.Label(self.info_frame, textvariable=self.resumen_text, 
                                    justify="left", bg="white", font=("Segoe UI", 11), fg="#333")
        self.lbl_resumen.pack(anchor="nw")



        # Botones alineados horizontalmente
        ttk.Button(self.toolbar, text="📥 Simulador Recibir", command=self.simular_recepcion, style="Tool.TButton").pack(side="left", padx=5, pady=5)
        ttk.Button(self.toolbar, text="📩 Ver Recibidos", command=self.ventana_bandeja_entrada, style="Tool.TButton").pack(side="left", padx=5, pady=5)
        ttk.Button(self.toolbar, text="📜 Historial Leídos", command=self.ventana_historial_leidos, style="Tool.TButton").pack(side="left", padx=5, pady=5)
        ttk.Button(self.toolbar, text="📝 Redactar email", command=self.ventana_enviar, style="Tool.TButton").pack(side="left", padx=5, pady=5)
        ttk.Button(self.toolbar, text="👤 +Contacto", command=self.ventana_contacto, style="Tool.TButton").pack(side="left", padx=5, pady=5)
        ttk.Button(self.toolbar, text="📇 Ver Contactos", command=self.ventana_ver_contactos, style="Tool.TButton").pack(side="left", padx=5, pady=5)

    def obtener_resumen(self):
        """Retorna el string con las estadísticas actuales usando los métodos del cliente [cite: 140, 141]"""
        return (f"👤 Usuario: {self.cliente.cuenta.usuario}\n"
                f"📧 Dirección: {self.cliente.cuenta.direccion}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"📊 Estadística de Correos:\n"
                f"   • Total de correos: {self.cliente.cantidad_total_correos()}\n"
                f"   • Recibidos: {self.cliente.cantidad_recibidos()}\n"
                f"   • Mensajes sin leer: {self.cliente.cantidad_no_leidos()}\n"
                f"   • Agenda de contactos: {len(self.cliente.contactos)}")
         
    def ventana_ver_contactos(self):
        """Punto 1: Muestra los contactos en formato tabla (Treeview)"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Agenda de Contactos")
        ventana.geometry("500x300")

        # Configuración de la Tabla (Treeview)
        columnas = ("nombre", "apellido", "email")
        tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
        
        # Definir encabezados
        tabla.heading("nombre", text="Nombre")
        tabla.heading("apellido", text="Apellido")
        tabla.heading("email", text="Correo Electrónico")
        
        # Ajustar ancho de columnas
        tabla.column("nombre", width=100)
        tabla.column("apellido", width=100)
        tabla.column("email", width=250)

        # Cargar datos desde la lista de objetos 'contactos' del cliente
        for con in self.cliente.contactos:
            tabla.insert("", tk.END, values=(con.nombre, con.apellido, con.email))

        tabla.pack(expand=True, fill="both", padx=10, pady=10)

    def ventana_historial_leidos(self):
        """Punto 2: Permite ver y volver a abrir mensajes ya leídos"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Mensajes Leídos")
        ventana.geometry("400x400")

        tk.Label(ventana, text="Historial de Mensajes Leídos", font=("Arial", 10, "bold")).pack(pady=5)

        lista_leidos = tk.Listbox(ventana, width=50, height=15)
        lista_leidos.pack(pady=5, padx=10)

        # Filtramos los objetos que tienen la propiedad leido = True
        objetos_filtrados = [c for c in self.cliente.recibidos if c.leido]

        for correo in objetos_filtrados:
            lista_leidos.insert(tk.END, f"✅ {correo.asunto} - De: {correo.remitente}")

        def abrir_seleccionado():
            indice = lista_leidos.curselection()
            if indice:
                correo_obj = objetos_filtrados[indice[0]]
                # Reutilizamos tu lógica de lectura de detalle
                self.mostrar_contenido_correo(correo_obj)

        tk.Button(ventana, text="Abrir de nuevo", command=abrir_seleccionado, bg="#67addb", fg="white").pack(pady=5)

    def mostrar_contenido_correo(self, correo_obj):
        """Método auxiliar para mostrar el cuerpo del mensaje"""
        v_lectura = tk.Toplevel(self.root)
        v_lectura.title(f"Re-leyendo: {correo_obj.asunto}")
        v_lectura.geometry("350x250")
        
        tk.Label(v_lectura, text=f"Asunto: {correo_obj.asunto}", font=("bold")).pack(pady=5)
        txt = tk.Text(v_lectura, height=8, width=40)
        txt.insert(tk.END, correo_obj.mensaje)
        txt.config(state="disabled")
        txt.pack(padx=10, pady=10)

 
    def actualizar_interfaz(self):
        self.resumen_text.set(self.obtener_resumen())

    def simular_recepcion(self):
        # Creamos una instancia de Correo
        nuevo = Correo("Aviso de Examen", "El parcial es el lunes 17:00hs. ", "Paula@unsada.edu.ar", [self.cliente.cuenta.direccion])
        self.cliente.recibidos.append(nuevo)
        self.actualizar_interfaz()
        messagebox.showinfo("Bandeja de Entrada", "Has recibido un nuevo correo de Paula.")

    def ventana_contacto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Nuevo Contacto")
        ventana.geometry("300x200")
        
        tk.Label(ventana, text="Nombre:").pack()
        ent_nom = tk.Entry(ventana)
        ent_nom.pack()
        
        tk.Label(ventana, text="Apellido:").pack()
        ent_ape = tk.Entry(ventana)
        ent_ape.pack()
        
        tk.Label(ventana, text="Email:").pack()
        ent_mail = tk.Entry(ventana)
        ent_mail.pack()

        def guardar():
            nuevo_con = Contacto(ent_nom.get(), ent_ape.get(), "", ent_mail.get())
            self.cliente.agregar_contacto_db(nuevo_con) 
            self.actualizar_interfaz()
            ventana.destroy()
            messagebox.showinfo("Éxito", "Contacto guardado en la base de datos.")

        tk.Button(ventana, text="Guardar", command=guardar, bg="#27ae60", fg="white").pack(pady=10)

    def ventana_enviar(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Redactar Nuevo Correo")
        ventana.geometry("400x350")
        ventana.configure(pady=10, padx=10)

        tk.Label(ventana, text="Para (Destinatario):").pack(anchor="w")
        ent_para = tk.Entry(ventana, width=40)
        ent_para.pack(pady=5)

        tk.Label(ventana, text="Asunto:").pack(anchor="w")
        ent_asunto = tk.Entry(ventana, width=40)
        ent_asunto.pack(pady=5)

        tk.Label(ventana, text="Mensaje:").pack(anchor="w")
        txt_mensaje = tk.Text(ventana, height=5, width=40)
        txt_mensaje.pack(pady=5)

        def procesar_envio():
            # Definimos atributos del objeto Correo
            nuevo_envio = Correo(
                asunto=ent_asunto.get(),
                mensaje=txt_mensaje.get("1.0", tk.END),
                remitente=self.cliente.cuenta.direccion,
                destinatarios=[ent_para.get()], 
                leido=True 
            )
            
            # El objeto realiza la acción de enviar
            self.cliente.enviar_correo(nuevo_envio)
            self.actualizar_interfaz()
            ventana.destroy()
            messagebox.showinfo("Enviado", "El correo se ha movido a la carpeta de Enviados.")

        tk.Button(ventana, text="🚀 Enviar Ahora", command=procesar_envio, 
                  bg="#67addb", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
    
    def ventana_bandeja_entrada(self):
        # Creamos ventana para listar los objetos Correo
        self.ventana_lista = tk.Toplevel(self.root)
        self.ventana_lista.title("Bandeja de Entrada")
        self.ventana_lista.geometry("400x400")

        tk.Label(self.ventana_lista, text="Correos Recibidos", font=("Arial", 12, "bold")).pack(pady=10)

        # Listbox para visualizar la colección de objetos
        self.lista_visual = tk.Listbox(self.ventana_lista, width=50, height=15)
        self.lista_visual.pack(pady=5, padx=10)

        # Accedemos a las propiedades de cada objeto en la lista
        for correo in self.cliente.recibidos:
            estado = "[LEÍDO]" if correo.leido else "[NUEVO]"
            self.lista_visual.insert(tk.END, f"{estado} {correo.asunto} - De: {correo.remitente}")

        tk.Button(self.ventana_lista, text="📖 Leer Correo Seleccionado", 
                  command=self.leer_correo_detalle, bg="#d67dbc").pack(pady=10)

    def leer_correo_detalle(self):
        seleccion = self.lista_visual.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccioná un correo de la lista.")
            return

        indice = seleccion[0]
        correo_obj = self.cliente.recibidos[indice]

        # Cambiamos el valor de la propiedad 'leido' 
        correo_obj.leido = True
        self.actualizar_interfaz() 

        ventana_lectura = tk.Toplevel(self.ventana_lista)
        ventana_lectura.title(f"Leyendo: {correo_obj.asunto}")
        ventana_lectura.geometry("350x300")

        tk.Label(ventana_lectura, text=f"De: {correo_obj.remitente}", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=5)
        tk.Label(ventana_lectura, text=f"Asunto: {correo_obj.asunto}").pack(anchor="w", padx=10)
        
        cuerpo = tk.Text(ventana_lectura, height=10, width=40)
        cuerpo.insert(tk.END, correo_obj.mensaje)
        cuerpo.config(state="disabled") 
        cuerpo.pack(pady=10, padx=10)
        
        ventana_lectura.bind("<Destroy>", lambda e: self.refrescar_bandeja())

    def refrescar_bandeja(self):
        self.lista_visual.delete(0, tk.END)
        for correo in self.cliente.recibidos:
            estado = "[LEÍDO]" if correo.leido else "[NUEVO]"
            self.lista_visual.insert(tk.END, f"{estado} {correo.asunto} - De: {correo.remitente}")
            
if __name__ == "__main__":
    from Cliente_Correo import Cuenta
    root = tk.Tk()
    mi_cuenta = Cuenta("Grupo2 Arrecifes", "Grupo2_arrecifes@estudiante.unsada.edu.ar", "pop.gmail.com", "smtp.gmail.com")
    mi_cliente = ClienteCorreo(mi_cuenta)
    
    app = AppCorreo(root, mi_cliente)
    root.mainloop()
