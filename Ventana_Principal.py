import tkinter as tk
from tkinter import messagebox, ttk 
import json
import os
from Cliente_Correo import ClienteCorreo, Cuenta

# --- CLASES VIRTUALES CON CAPACIDAD DE GUARDADO ---
class ContactoVirtual:
    def __init__(self, nombre, apellido, correo):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.email = correo 

    def to_dict(self):
        return {"nombre": self.nombre, "apellido": self.apellido, "correo": self.correo}

class CorreoVirtual:
    def __init__(self, remitente, destinatario, asunto, mensaje, leido=False):
        self.remitente = remitente
        self.destinatario = destinatario
        self.asunto = asunto
        self.mensaje = mensaje
        self.cuerpo = mensaje
        self.leido = leido 

    def to_dict(self):
        return {"remitente": self.remitente, "destinatario": self.destinatario, "asunto": self.asunto, "mensaje": self.mensaje, "leido": self.leido}

class AppCorreo:
    def __init__(self, root, cliente):
        self.cliente = cliente
        self.root = root
        
        self.usuario = getattr(cliente.cuenta, 'usuario', 'Usuario')
        self.direccion = getattr(cliente.cuenta, 'direccion', 'correo@unsada.edu.ar')
        
        # Iniciamos listas vacías
        self.correos_recibidos = []
        self.correos_enviados = []
        self.contactos = []

        # Intentamos cargar los datos guardados de la sesión anterior
        self.cargar_datos_locales()

        self.root.title(f"UNSADA Mail Pro - {self.usuario}")
        self.root.geometry("850x600") 
        self.root.configure(bg="#f0f2f5")

        self.construir_interfaz()

    # --- SISTEMA DE GUARDADO AUTOMÁTICO (PERSISTENCIA) ---
    def cargar_datos_locales(self):
        if os.path.exists("datos_app.json"):
            try:
                with open("datos_app.json", "r") as f:
                    data = json.load(f)
                    self.contactos = [ContactoVirtual(**c) for c in data.get("contactos", [])]
                    self.correos_recibidos = [CorreoVirtual(**c) for c in data.get("recibidos", [])]
                    self.correos_enviados = [CorreoVirtual(**c) for c in data.get("enviados", [])]
            except Exception:
                pass # Si falla, simplemente inicia en blanco

    def guardar_datos_locales(self):
        data = {
            "contactos": [c.to_dict() for c in self.contactos],
            "recibidos": [c.to_dict() for c in self.correos_recibidos],
            "enviados": [c.to_dict() for c in self.correos_enviados]
        }
        with open("datos_app.json", "w") as f:
            json.dump(data, f)

    def construir_interfaz(self):
        # --- ENCABEZADO ---
        header = tk.Frame(self.root, bg="#14b685", height=70) 
        header.pack(fill="x")
        
        tk.Label(header, text="✨ UNSADA Mail Pro", bg="#14b685", fg="white", 
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=25, pady=15)
        tk.Label(header, text=self.direccion, bg="#14b685", fg="#d1f2e6", 
                 font=("Segoe UI", 11, "italic")).pack(side="right", padx=25, pady=15)

        # --- BARRA DE HERRAMIENTAS ---
        toolbar = tk.Frame(self.root, bg="white", pady=10, highlightbackground="#dcdde1", highlightthickness=1)
        toolbar.pack(fill="x")

        frame_correos = tk.Frame(toolbar, bg="white")
        frame_correos.pack(side="left", padx=15)
        
        frame_contactos = tk.Frame(toolbar, bg="white")
        frame_contactos.pack(side="right", padx=15)

        btn_style = {"font": ("Segoe UI", 9, "bold"), "fg": "white", "bg": "#2c3e50", "relief": "flat", "padx": 10, "pady": 6, "cursor": "hand2"}
        btn_green = {"font": ("Segoe UI", 9, "bold"), "fg": "white", "bg": "#14b685", "relief": "flat", "padx": 10, "pady": 6, "cursor": "hand2"}

        tk.Button(frame_correos, text="📥 Recibir", command=self.simular_recepcion, **btn_style).pack(side="left", padx=5)
        tk.Button(frame_correos, text="📩 Recibidos", command=self.ver_recibidos, **btn_style).pack(side="left", padx=5)
        tk.Button(frame_correos, text="📤 Enviados", command=self.ver_enviados, **btn_style).pack(side="left", padx=5)
        tk.Button(frame_correos, text="📝 Redactar", command=self.ventana_enviar, **btn_green).pack(side="left", padx=15)

        tk.Button(frame_contactos, text="👥 Ver Contactos", command=self.ver_contactos, **btn_style).pack(side="left", padx=5)
        tk.Button(frame_contactos, text="➕ Nuevo Contacto", command=self.agregar_contacto, **btn_green).pack(side="left", padx=5)

        # --- PANEL CENTRAL ---
        self.content = tk.Frame(self.root, bg="#f0f2f5", padx=40, pady=30)
        self.content.pack(fill="both", expand=True)

        self.actualizar_dashboard()

    def actualizar_dashboard(self):
        for widget in self.content.winfo_children():
            widget.destroy()

        card = tk.Frame(self.content, bg="white", highlightbackground="#14b685", highlightthickness=2)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="📌 Panel de Control y Estadísticas", font=("Segoe UI", 16, "bold"), 
                 bg="white", fg="#14b685").pack(anchor="w", padx=30, pady=(25, 10))
        
        tk.Frame(card, bg="#eeeeee", height=2).pack(fill="x", padx=30, pady=10)

        total_correos = len(self.correos_recibidos) + len(self.correos_enviados)
        recibidos = len(self.correos_recibidos)
        enviados = len(self.correos_enviados)
        contactos = len(self.contactos)
        no_leidos = sum(1 for c in self.correos_recibidos if getattr(c, 'leido', False) == False)

        texto_resumen = (f"👤 Cuenta activa: {self.usuario}\n\n"
                         f"📊 Tu actividad al momento:\n"
                         f"    • Total de correos: {total_correos}\n"
                         f"    • Correos Recibidos: {recibidos}\n"
                         f"    • Correos Enviados: {enviados}\n"
                         f"    • Correos No Leídos: {no_leidos}\n"
                         f"    • Contactos Guardados: {contactos}")
        
        tk.Label(card, text=texto_resumen, font=("Segoe UI", 12), bg="white", 
                 fg="#333333", justify="left").pack(anchor="w", padx=40, pady=10)

    # ==========================================
    # FUNCIONES (CON GUARDADO AUTOMÁTICO)
    # ==========================================

    def agregar_contacto(self):
        v = tk.Toplevel(self.root)
        v.title("Nuevo Contacto")
        v.geometry("500x350")
        v.configure(bg="white")
        
        tk.Label(v, text="Nombre:", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=25, pady=(20,2))
        ent_nom = tk.Entry(v, width=45, bg="#f8f9fa", relief="solid", bd=1); ent_nom.pack()
        tk.Label(v, text="Apellido:", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=25, pady=(20,2))
        ent_ape = tk.Entry(v, width=45, bg="#f8f9fa", relief="solid", bd=1); ent_ape.pack()
        tk.Label(v, text="Correo Electrónico:", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=25, pady=(10,2))
        ent_cor = tk.Entry(v, width=45, bg="#f8f9fa", relief="solid", bd=1); ent_cor.pack()
        
        def guardar():
            n = ent_nom.get()
            a = ent_ape.get()
            c = ent_cor.get()
            if n and c:
                nuevo = ContactoVirtual(n, c)
                self.contactos.append(nuevo)
                self.guardar_datos_locales() 
                messagebox.showinfo("Éxito", f"El contacto {n} fue guardado correctamente.")
                self.actualizar_dashboard()
                v.destroy()
            else:
                messagebox.showwarning("Error", "Completa todos los campos.")
                
        tk.Button(v, text="💾 Guardar Contacto", command=guardar, bg="#14b685", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=5).pack(pady=20)

    def ver_contactos(self):
        v = tk.Toplevel(self.root)
        v.title("Mi Libreta de Direcciones")
        v.geometry("600x350")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#14b685", foreground="white")

        tree = ttk.Treeview(v, columns=("Nombre", "Apellido", "Correo"), show="headings")
        tree.heading("Nombre", text="Nombre del Contacto")
        tree.heading("Apellido", text="Apellido del Contacto")
        tree.heading("Correo", text="Correo Electrónico")
        tree.pack(fill="both", expand=True, padx=15, pady=15)
        
        for c in self.contactos:
            tree.insert("", "end", values=(c.nombre, c.apellido, c.correo))

    def simular_recepcion(self):
        nuevo_correo = CorreoVirtual("Rectorado UNSADA", self.direccion, "Novedades del cuatrimestre", "Estimado alumno, le informamos que las mesas de exámenes están habilitadas. ¡Saludos!")
        self.correos_recibidos.append(nuevo_correo)
        self.guardar_datos_locales() 
        self.actualizar_dashboard()
        messagebox.showinfo("Servidor Actualizado", "📥 Has recibido 1 correo nuevo. Revisa tu bandeja de entrada.")

    def ventana_enviar(self):
        v = tk.Toplevel(self.root)
        v.title("Redactar Correo")
        v.geometry("500x450")
        v.configure(bg="white")
        
        tk.Label(v, text="Para (Elige un contacto o escribe):", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=25, pady=(20,2))
        
        lista_emails = [c.correo for c in self.contactos]
        ent_p = ttk.Combobox(v, values=lista_emails, width=52)
        ent_p.pack()
        
        tk.Label(v, text="Asunto:", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=25, pady=(10,2))
        ent_a = tk.Entry(v, width=55, bg="#f8f9fa", relief="solid", bd=1); ent_a.pack()
        
        tk.Label(v, text="Mensaje:", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=25, pady=(10,2))
        txt = tk.Text(v, height=10, width=55, bg="#f8f9fa", relief="solid", bd=1); txt.pack()
        
        def enviar():
            dest = ent_p.get()
            asu = ent_a.get()
            msj = txt.get("1.0", tk.END).strip()
            if dest and asu:
                nuevo = CorreoVirtual(self.direccion, dest, asu, msj)
                self.correos_enviados.append(nuevo)
                self.guardar_datos_locales() 
                messagebox.showinfo("Enviado", "🚀 El correo fue enviado con éxito.")
                self.actualizar_dashboard()
                v.destroy()
            else:
                messagebox.showwarning("Faltan datos", "Debes ingresar destinatario y asunto.")
                
        tk.Button(v, text="Enviar Correo", command=enviar, bg="#14b685", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=8).pack(pady=15)

    def crear_ventana_lectura(self, titulo, lista_correos, es_recibido=True):
        v = tk.Toplevel(self.root)
        v.title(titulo)
        v.geometry("700x400")
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#14b685", foreground="white")

        col_persona = "De" if es_recibido else "Para"
        tree = ttk.Treeview(v, columns=(col_persona, "Asunto"), show="headings")
        tree.heading(col_persona, text=f"Correo {col_persona}")
        tree.heading("Asunto", text="Asunto")
        tree.column(col_persona, width=200)
        tree.column("Asunto", width=450)
        tree.pack(fill="both", expand=True, padx=15, pady=15)
        
        for c in lista_correos:
            persona = c.remitente if es_recibido else c.destinatario
            tree.insert("", "end", values=(persona, c.asunto))
            
        def leer():
            seleccion = tree.selection()
            if seleccion:
                # ACÁ ESTÁ LA MAGIA: Buscamos por la posición exacta (índice) en la tabla
                indice = tree.index(seleccion[0])
                correo_seleccionado = lista_correos[indice]
                
                # Si lo leés y estaba sin leer, se marca y se descuenta
                if es_recibido and not correo_seleccionado.leido:
                    correo_seleccionado.leido = True
                    self.guardar_datos_locales()
                    self.actualizar_dashboard()
                        
                etiqueta_pers = "Remitente" if es_recibido else "Destinatario"
                persona = correo_seleccionado.remitente if es_recibido else correo_seleccionado.destinatario
                messagebox.showinfo(f"Lectura de Correo", f"{etiqueta_pers}: {persona}\nAsunto: {correo_seleccionado.asunto}\n\n{'-'*40}\n{correo_seleccionado.mensaje}")
            else:
                messagebox.showwarning("Atención", "Selecciona un correo para leerlo.")
                
        tk.Button(v, text="📖 Abrir Mensaje", command=leer, bg="#2c3e50", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=8).pack(pady=(0,15))

    def ver_recibidos(self):
        self.crear_ventana_lectura("Bandeja de Entrada", self.correos_recibidos, es_recibido=True)

    def ver_enviados(self):
        self.crear_ventana_lectura("Bandeja de Salida (Enviados)", self.correos_enviados, es_recibido=False)

if __name__ == "__main__":
    root = tk.Tk()
    mi_cuenta = Cuenta("Grupo2 Arrecifes", "Grupo2_arrecifes@estudiante.unsada.edu.ar", "pop.gmail.com", "smtp.gmail.com")
    mi_cliente = ClienteCorreo(mi_cuenta)
    app = AppCorreo(root, mi_cliente)
    root.mainloop()