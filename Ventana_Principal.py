import tkinter as tk
from Connectar_bd import obtener_conexion
from tkinter import messagebox, ttk 
from Cliente_Correo import ClienteCorreo, Cuenta, Correo, Contacto

class AppCorreo:
    def __init__(self, root, cliente):
        self.cliente = cliente
        self.root = root
        self.root.title(f"UNSADA Mail - {self.cliente.cuenta.usuario}")
        self.root.geometry("600x550") # Aumentamos un poco el alto para que entre todo cómodo
        self.root.configure(bg="#f0f0f0")

        # --- Encabezado ---
        self.header = tk.Frame(root, bg="#2c3e50", height=60)
        self.header.pack(fill="x")
        
        tk.Label(self.header, text="Mi Correo Electrónico", bg="#2c3e50", fg="white", 
                 font=("Arial", 16, "bold")).pack(pady=10)

        # --- Panel de Información (Atributos del Objeto) ---
        self.info_frame = tk.LabelFrame(root, text=" Estado de la Cuenta ", padx=20, pady=10, bg="white")
        self.info_frame.pack(pady=20, padx=20, fill="x")

        self.resumen_text = tk.StringVar()
        self.resumen_text.set(self.obtener_resumen())
        
        self.lbl_resumen = tk.Label(self.info_frame, textvariable=self.resumen_text, 
                                    justify="left", bg="white", font=("Courier", 10))
        self.lbl_resumen.pack(side="left")

        # --- Panel de Acciones (Métodos del Objeto) ---
        self.btn_frame = tk.Frame(root, bg="#f0f0f0")
        self.btn_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10))

        # Fila 0: Botones principales
        ttk.Button(self.btn_frame, text="📥 Recibir Correo", command=self.simular_recepcion).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.btn_frame, text="📝 Enviar Correo", command=self.ventana_enviar).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.btn_frame, text="👤 Agregar Contacto", command=self.ventana_contacto).grid(row=0, column=2, padx=5, pady=5)

        # Fila 1: Botón de Visualización (EL QUE PEDISTE AGREGAR)
        ttk.Button(self.btn_frame, text="📩 Ver Recibidos", 
                   command=self.ventana_bandeja_entrada).grid(row=1, column=1, pady=15)

    def obtener_resumen(self):
        # Acciones requeridas por la consigna [cite: 175, 180]
        return (f"Usuario: {self.cliente.cuenta.usuario}\n"
                f"----------------------------------\n"
                f"Total de correos: {self.cliente.cantidad_total_correos()}\n"
                f"Recibidos: {self.cliente.cantidad_recibidos()}\n"
                f"No leídos: {self.cliente.cantidad_no_leidos()}\n"
                f"Contactos: {len(self.cliente.contactos)}")

    def actualizar_interfaz(self):
        self.resumen_text.set(self.obtener_resumen())

    def simular_recepcion(self):
        # Creamos una instancia de Correo [cite: 230]
        nuevo = Correo("Aviso de Examen", "El parcial es el lunes.", "bedelia@unsada.edu.ar", [self.cliente.cuenta.direccion])
        self.cliente.recibidos.append(nuevo)
        self.actualizar_interfaz()
        messagebox.showinfo("Bandeja de Entrada", "Has recibido un nuevo correo de Bedelía.")

    def ventana_contacto(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Nuevo Contacto")
        ventana.geometry("300x200")
        
        tk.Label(ventana, text="Nombre:").pack()
        ent_nom = tk.Entry(ventana)
        ent_nom.pack()
        
        tk.Label(ventana, text="Email:").pack()
        ent_mail = tk.Entry(ventana)
        ent_mail.pack()

        def guardar():
            nuevo_con = Contacto(ent_nom.get(), "", ent_mail.get())
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
            # Definimos atributos del objeto Correo [cite: 40, 198]
            nuevo_envio = Correo(
                asunto=ent_asunto.get(),
                mensaje=txt_mensaje.get("1.0", tk.END),
                remitente=self.cliente.cuenta.direccion,
                destinatarios=[ent_para.get()], 
                leido=True 
            )
            
            # El objeto realiza la acción de enviar [cite: 141, 218]
            self.cliente.enviar_correo(nuevo_envio)
            self.actualizar_interfaz()
            ventana.destroy()
            messagebox.showinfo("Enviado", "El correo se ha movido a la carpeta de Enviados.")

        tk.Button(ventana, text="🚀 Enviar Ahora", command=procesar_envio, 
                  bg="#3498db", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
    
    def ventana_bandeja_entrada(self):
        # Creamos ventana para listar los objetos Correo [cite: 140, 228]
        self.ventana_lista = tk.Toplevel(self.root)
        self.ventana_lista.title("Bandeja de Entrada")
        self.ventana_lista.geometry("400x400")

        tk.Label(self.ventana_lista, text="Correos Recibidos", font=("Arial", 12, "bold")).pack(pady=10)

        # Listbox para visualizar la colección de objetos [cite: 175]
        self.lista_visual = tk.Listbox(self.ventana_lista, width=50, height=15)
        self.lista_visual.pack(pady=5, padx=10)

        # Accedemos a las propiedades de cada objeto en la lista [cite: 291, 293]
        for correo in self.cliente.recibidos:
            estado = "[LEÍDO]" if correo.leido else "[NUEVO]"
            self.lista_visual.insert(tk.END, f"{estado} {correo.asunto} - De: {correo.remitente}")

        tk.Button(self.ventana_lista, text="📖 Leer Correo Seleccionado", 
                  command=self.leer_correo_detalle, bg="#f1c40f").pack(pady=10)

    def leer_correo_detalle(self):
        seleccion = self.lista_visual.curselection()
        if not seleccion:
            messagebox.showwarning("Atención", "Por favor, seleccioná un correo de la lista.")
            return

        indice = seleccion[0]
        correo_obj = self.cliente.recibidos[indice]

        # Cambiamos el valor de la propiedad 'leido' [cite: 294]
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
    mi_cuenta = Cuenta("Mónica_Informatica", "moni@estudiante.unsada.edu.ar", "pop.gmail.com", "smtp.gmail.com")
    mi_cliente = ClienteCorreo(mi_cuenta)
    
    app = AppCorreo(root, mi_cliente)
    root.mainloop()
