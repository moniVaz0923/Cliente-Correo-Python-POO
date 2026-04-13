import tkinter as tk
from tkinter import messagebox, ttk 
import json
import os

# --- CLASES VIRTUALES (Persistencia asegurada) ---
class ContactoVirtual:
    def __init__(self, nombre, apellido,correo):
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo

    def to_dict(self):
        return {"nombre": self.nombre, "apellido": self.apellido, "correo": self.correo}

class CorreoVirtual:
    def __init__(self, remitente, destinatario, asunto, mensaje, leido=False):
        self.remitente = remitente
        self.destinatario = destinatario
        self.asunto = asunto
        self.mensaje = mensaje
        self.leido = leido 

    def to_dict(self):
        return {"remitente": self.remitente, "destinatario": self.destinatario, "asunto": self.asunto, "mensaje": self.mensaje, "leido": self.leido}

class AppCorreo:
    def __init__(self, root):
        self.root = root
        self.usuario = "Grupo2 Arrecifes"
        self.direccion = "Grupo2_arrecifes@estudiante.unsada.edu.ar"
        
        self.correos_recibidos = []
        self.correos_enviados = []
        self.contactos = []

        self.cargar_datos_locales()

        self.root.title("UNSADA Mail Pro - Grupo2 Arrecifes")
        self.root.geometry("950x650") 
        self.root.configure(bg="#f0f2f5")

        self.mostrar_login()

    # --- SISTEMA DE LOGIN ---
    def mostrar_login(self):
        self.frame_login = tk.Frame(self.root, bg="#2c3e50")
        self.frame_login.pack(fill="both", expand=True)

        tarjeta = tk.Frame(self.frame_login, bg="white", padx=40, pady=40, bd=0)
        tarjeta.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(tarjeta, text="🔒 UNSADA Mail Pro", font=("Segoe UI", 20, "bold"), bg="white", fg="#14b685").pack(pady=(0, 20))
        tk.Label(tarjeta, text="Ingresa tu contraseña para continuar\n(Contraseña: unsada2026)", font=("Segoe UI", 10), bg="white", fg="#7f8c8d").pack(pady=(0, 20))

        self.ent_pass = tk.Entry(tarjeta, font=("Segoe UI", 14), show="*", justify="center", bg="#f0f2f5", relief="flat")
        self.ent_pass.pack(pady=10, fill="x", ipady=5)

        def verificar(evento=None):
            if self.ent_pass.get() == "unsada2026":
                self.frame_login.destroy()
                self.construir_interfaz()
            else:
                messagebox.showerror("Error", "❌ Contraseña incorrecta.")
                self.ent_pass.delete(0, 'end')

        tk.Button(tarjeta, text="Iniciar Sesión", command=verificar, bg="#14b685", fg="white", font=("Segoe UI", 12, "bold"), relief="flat", cursor="hand2").pack(fill="x", pady=(20, 0), ipady=5)
        self.root.bind('<Return>', verificar)

    # --- PERSISTENCIA (JSON) ---
    def cargar_datos_locales(self):
        if os.path.exists("datos_app.json"):
            try:
                with open("datos_app.json", "r") as f:
                    data = json.load(f)
                    self.contactos = [ContactoVirtual(**c) for c in data.get("contactos", [])]
                    self.correos_recibidos = [CorreoVirtual(**c) for c in data.get("recibidos", [])]
                    self.correos_enviados = [CorreoVirtual(**c) for c in data.get("enviados", [])]
            except Exception: pass

    def guardar_datos_locales(self):
        data = {
            "contactos": [c.to_dict() for c in self.contactos],
            "recibidos": [c.to_dict() for c in self.correos_recibidos],
            "enviados": [c.to_dict() for c in self.correos_enviados]
        }
        with open("datos_app.json", "w") as f:
            json.dump(data, f, indent=4)

    # --- INTERFAZ PRINCIPAL ---
    def construir_interfaz(self):
        self.root.unbind('<Return>')
        
        # Header
        header = tk.Frame(self.root, bg="#14b685", height=70) 
        header.pack(fill="x")
        tk.Label(header, text="✨ UNSADA Mail Pro", bg="#14b685", fg="white", font=("Segoe UI", 18, "bold")).pack(side="left", padx=25, pady=15)
        tk.Label(header, text=self.direccion, bg="#14b685", fg="#d1f2e6", font=("Segoe UI", 11, "italic")).pack(side="right", padx=25, pady=15)

        # Toolbar
        toolbar = tk.Frame(self.root, bg="white", pady=10, bd=1, relief="flat")
        toolbar.pack(fill="x")

        frame_izq = tk.Frame(toolbar, bg="white")
        frame_izq.pack(side="left", padx=15)
        frame_der = tk.Frame(toolbar, bg="white")
        frame_der.pack(side="right", padx=15)

        btn_s = {"font": ("Segoe UI", 9, "bold"), "fg": "white", "bg": "#2c3e50", "relief": "flat", "padx": 10, "pady": 6, "cursor": "hand2"}
        btn_g = {**btn_s, "bg": "#14b685"}
        btn_r = {**btn_s, "bg": "#e74c3c"}

        tk.Button(frame_izq, text="📥 Recibir", command=self.simular_recepcion, **btn_s).pack(side="left", padx=5)
        tk.Button(frame_izq, text="📩 Recibidos", command=self.ver_recibidos, **btn_s).pack(side="left", padx=5)
        tk.Button(frame_izq, text="📤 Enviados", command=self.ver_enviados, **btn_s).pack(side="left", padx=5)
        tk.Button(frame_izq, text="📝 Redactar", command=lambda: self.ventana_enviar(), **btn_g).pack(side="left", padx=15)
        tk.Button(frame_der, text="🗑️ Vaciar e-mail ", command=self.borrar_historial_total, **btn_r).pack(side="left", padx=15)

        tk.Button(frame_der, text="👥 Ver Contactos", command=self.ver_contactos, **btn_s).pack(side="left", padx=5)
        tk.Button(frame_der, text="➕ Nuevo Contacto", command=self.agregar_contacto, **btn_g).pack(side="left", padx=5)
        

        # Dashboard
        self.content = tk.Frame(self.root, bg="#f0f2f5", padx=40, pady=30)
        self.content.pack(fill="both", expand=True)
        self.actualizar_dashboard()

    def actualizar_dashboard(self):
        for w in self.content.winfo_children(): w.destroy()
        card = tk.Frame(self.content, bg="white", highlightbackground="#14b685", highlightthickness=2)
        card.pack(fill="both", expand=True)
        
        tk.Label(card, text="📌 Panel de Control y Estadísticas", font=("Segoe UI", 16, "bold"), bg="white", fg="#14b685").pack(anchor="w", padx=30, pady=(25, 10))
        tk.Frame(card, bg="#eeeeee", height=2).pack(fill="x", padx=30, pady=10)

        # Lógica exacta para el TP
        total_correos = len(self.correos_recibidos) + len(self.correos_enviados)
        recibidos = len(self.correos_recibidos)
        enviados = len(self.correos_enviados)
        contactos = len(self.contactos)
        # Calcula los no leídos
        no_leidos = sum(1 for c in self.correos_recibidos if not c.leido)

        texto_resumen = (f"👤 Cuenta activa: {self.usuario}\n\n"
                         f"📊 Tu actividad al momento:\n"
                         f"    • Total de correos: {total_correos}\n"
                         f"    • Correos Recibidos: {recibidos}\n"
                         f"    • Correos Enviados: {enviados}\n"
                         f"    • Correos No Leídos: {no_leidos}\n"
                         f"    • Contactos Guardados: {contactos}")
        
        tk.Label(card, text=texto_resumen, font=("Segoe UI", 12), bg="white", fg="#333333", justify="left").pack(anchor="w", padx=40, pady=10)

    # --- FUNCIONES DEL TP ---
    def agregar_contacto(self):
        v = tk.Toplevel(self.root)
        v.title("Nuevo Contacto")
        v.geometry("600x250")
        v.configure(bg="white")
        
        tk.Label(v, text="Nombre:", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=25, pady=(20,2))
        ent_nom = tk.Entry(v, width=45, bg="#f8f9fa", relief="solid", bd=1); ent_nom.pack()
        
        tk.Label(v, text="Apellido:", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=25, pady=(10,2))
        ent_ape = tk.Entry(v, width=45, bg="#f8f9fa", relief="solid", bd=1); ent_ape.pack()
        
        tk.Label(v, text="Correo Electrónico:", bg="white", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=25, pady=(10,2))
        ent_cor = tk.Entry(v, width=45, bg="#f8f9fa", relief="solid", bd=1); ent_cor.pack()
        
        def guardar():
            n = ent_nom.get()
            a = ent_ape.get()
            c = ent_cor.get()
            if n and a and c:
                self.contactos.append(ContactoVirtual(n, a, c))
                self.guardar_datos_locales() 
                messagebox.showinfo("Éxito", f"El contacto {n} fue guardado.")
                self.actualizar_dashboard()
                v.destroy()
            else:
                messagebox.showwarning("Error", "Completa todos los campos.")
                
        tk.Button(v, text="💾 Guardar Contacto", command=guardar, bg="#14b685", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=5).pack(pady=20)

    def simular_recepcion(self):
        nuevo_correo = CorreoVirtual(
            remitente="Rectorado UNSADA", 
            destinatario=self.direccion, 
            asunto="Novedades de la cursada", 
            mensaje="Hola grupo, les avisamos que ya están cargadas las notas. ¡Saludos!"
        )
        self.correos_recibidos.append(nuevo_correo)
        self.guardar_datos_locales() 
        self.actualizar_dashboard()
        messagebox.showinfo("Buzón", "📥 ¡Llegó un correo nuevo!")

    def ver_contactos(self):
        v = tk.Toplevel(self.root)
        v.title("Libreta de Direcciones")
        v.geometry("600x400")

        frame_tabla = tk.Frame(v)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        scrolly = tk.Scrollbar(frame_tabla)
        scrolly.pack(side="right", fill="y")
        
        tree = ttk.Treeview(frame_tabla, columns=("Nom", "Ape", "Cor"), show="headings", yscrollcommand=scrolly.set)
        tree.heading("Nom", text="Nombre");tree.heading("Ape", text="Apellido"); tree.heading("Cor", text="Correo")
        tree.pack(fill="both", expand=True)
        scrolly.config(command=tree.yview)

        for c in self.contactos:
            tree.insert("", "end", values=(c.nombre,c.apellido,c.correo))

        def eliminar():
            sel = tree.selection()
            if sel:
                idx = tree.index(sel[0])
                del self.contactos[idx]
                self.guardar_datos_locales()
                tree.delete(sel[0])
                self.actualizar_dashboard()

        tk.Button(v, text="🗑️ Eliminar Seleccionado", command=eliminar, bg="#e74c3c", fg="white").pack(pady=10)

    def ver_recibidos(self):
        self.ventana_correos("Bandeja de Entrada", self.correos_recibidos, True)

    def ver_enviados(self):
        self.ventana_correos("Enviados", self.correos_enviados, False)

    def ventana_correos(self, titulo, lista, es_recibido):
        v = tk.Toplevel(self.root)
        v.title(titulo)
        v.geometry("700x400")

        frame_tabla = tk.Frame(v)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        scrolly = tk.Scrollbar(frame_tabla)
        scrolly.pack(side="right", fill="y")
        
        col_pers = "De" if es_recibido else "Para"
        tree = ttk.Treeview(frame_tabla, columns=("Pers", "Asu"), show="headings", yscrollcommand=scrolly.set)
        tree.heading("Pers", text=col_pers); tree.heading("Asu", text="Asunto")
        tree.column("Pers", width=150); tree.column("Asu", width=400)
        tree.pack(fill="both", expand=True)
        scrolly.config(command=tree.yview)

        def refrescar():
            tree.delete(*tree.get_children())
            for c in lista:
                p = c.remitente if es_recibido else c.destinatario
                # Le agregamos un iconito si no está leído para que se note
                estado = "✉️ " if es_recibido and not c.leido else "📖 "
                tree.insert("", "end", values=(p, estado + c.asunto))
        refrescar()

        def abrir():
            sel = tree.selection()
            if sel:
                idx = tree.index(sel[0])
                item = lista[idx]
                
                # ACÁ ESTÁ LA MAGIA DE "NO LEÍDO" -> "LEÍDO"
                if es_recibido and not item.leido:
                    item.leido = True
                    self.guardar_datos_locales()
                    self.actualizar_dashboard()
                    refrescar() # Para sacarle el ícono de sobrecito cerrado

                vl = tk.Toplevel(v)
                vl.title("Lectura")
                vl.geometry("400x300")
                tk.Label(vl, text=f"Asunto: {item.asunto}", font=("bold")).pack(pady=10)
                txt = tk.Text(vl, height=8); txt.insert("1.0", item.mensaje); txt.pack(padx=10)
                
                if es_recibido:
                    tk.Button(vl, text="↩️ Resp1onder", bg="#14b685", fg="white", 
                              command=lambda: [vl.destroy(), self.ventana_enviar(item.remitente, f"Re: {item.asunto}")]).pack(pady=5)
        
        tk.Button(v, text="📖 Leer Mensaje", command=abrir, bg="#2c3e50", fg="white").pack(pady=10)

    def ventana_enviar(self, para="", asunto=""):
        v = tk.Toplevel(self.root)
        v.title("Redactar")
        v.geometry("450x450")
        
        tk.Label(v, text="Para (Elige o escribe):").pack(anchor="w", padx=20, pady=(10, 2))
        lista_emails = [c.correo for c in self.contactos]
        ent_p = ttk.Combobox(v, values=lista_emails)
        if para: ent_p.insert(0, para)
        ent_p.pack(fill="x", padx=20)
        
        tk.Label(v, text="Asunto:").pack(anchor="w", padx=20, pady=(10, 2))
        ent_a = tk.Entry(v)
        if asunto: ent_a.insert(0, asunto)
        ent_a.pack(fill="x", padx=20)
        
        tk.Label(v, text="Mensaje:").pack(anchor="w", padx=20, pady=(10, 2))
        txt = tk.Text(v, height=10)
        txt.pack(fill="both", padx=20, pady=5)

        def enviar():
            d = ent_p.get().strip()
            a = ent_a.get().strip()
            m = txt.get("1.0", "end").strip()
            if d and a:
                self.correos_enviados.append(CorreoVirtual(self.direccion, d, a, m))
                self.guardar_datos_locales()
                self.actualizar_dashboard()
                messagebox.showinfo("Enviado", "🚀 Correo enviado.")
                v.destroy()
            else:
                messagebox.showwarning("Atención", "Completá destinatario y asunto.")

        tk.Button(v, text="🚀 Enviar", command=enviar, bg="#14b685", fg="white", padx=20).pack(pady=10)

    def borrar_historial_total(self):
        if messagebox.askyesnocancel("Peligro", "¿Borrar TODOS los correos?"):
            self.correos_recibidos = []
            self.correos_enviados = []
            self.guardar_datos_locales()
            self.actualizar_dashboard()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppCorreo(root)
    root.mainloop()