import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
from mysql.connector import Error
import bcrypt
import re
from datetime import datetime
from cryptography.fernet import Fernet
import hashlib
import string
import secrets

class Config:
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Prince319*',
        'database': 'gestor_contrasenas',
        'auth_plugin': 'mysql_native_password'
    }

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection = None
            self.cursor = None
            self.cipher = None
            self.initialized = True
            self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(**Config.DB_CONFIG)
            self.cursor = self.connection.cursor(dictionary=True)
            print("Conexión a MySQL establecida")
            self.init_crypto()
            return True
        except Error as err:
            print(f"Error de conexión: {err}")
            return False
    
    def init_crypto(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS claves_cifrado (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    clave TEXT NOT NULL,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.connection.commit()
            
            self.cursor.execute("SELECT clave FROM claves_cifrado ORDER BY id DESC LIMIT 1")
            result = self.cursor.fetchone()
            
            if result and result['clave']:
                key = result['clave'].encode()
            else:
                key = Fernet.generate_key()
                self.cursor.execute("INSERT INTO claves_cifrado (clave) VALUES (%s)", (key.decode(),))
                self.connection.commit()
            
            self.cipher = Fernet(key)
            print("Cifrado inicializado")
        except Exception as e:
            print(f"Error inicializando cifrado: {e}")
            self.cipher = None
    
    def execute_query(self, query, params=None, fetch=False):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if fetch:
                result = self.cursor.fetchall()
                return result
            else:
                self.connection.commit()
                return self.cursor.rowcount
        except Error as e:
            print(f"Error en consulta: {e}")
            return None
    
    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

class Security:
    @staticmethod
    def hash_password(password):
        """Genera hash seguro de contraseña"""
        try:
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            print(f"Error generando hash: {e}")
            return None
    
    @staticmethod
    def verify_password(stored_hash, provided_password):
        """Verifica si la contraseña coincide con el hash"""
        try:
            if not stored_hash or not provided_password:
                return False
            
            if isinstance(stored_hash, str):
                stored_bytes = stored_hash.encode('utf-8')
            else:
                stored_bytes = stored_hash
            
            provided_bytes = provided_password.encode('utf-8')
            
            return bcrypt.checkpw(provided_bytes, stored_bytes)
        except Exception as e:
            print(f"Error verificando contraseña: {e}")
            return False
    
    @staticmethod
    def check_password_strength(password):
        """Verifica la fortaleza de la contraseña"""
        score = 0
        alerts = []
        
        if len(password) >= 8:
            score += 1
        else:
            alerts.append("Debe tener al menos 8 caracteres")
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            alerts.append("Falta letra mayúscula")
        
        if re.search(r'[a-z]', password):
            score += 1
        else:
            alerts.append("Falta letra minúscula")
        
        if re.search(r'[0-9]', password):
            score += 1
        else:
            alerts.append("Falta número")

        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        else:
            alerts.append("Falta carácter especial")
        
        if score == 5:
            strength = "Muy Fuerte"
            color = "#2ecc71"
        elif score >= 3:
            strength = "Fuerte"
            color = "#27ae60"
        elif score >= 2:
            strength = "Moderada"
            color = "#f39c12"
        else:
            strength = "Débil"
            color = "#e74c3c"
        
        return {
            'score': score,
            'strength': strength,
            'color': color,
            'alerts': alerts
        }
    
    @staticmethod
    def generate_strong_password(length=12):
        """Genera una contraseña fuerte"""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    @staticmethod
    def encrypt_text(text, cipher):
        """Encripta texto usando Fernet"""
        if cipher:
            return cipher.encrypt(text.encode()).decode()
        return text
    
    @staticmethod
    def decrypt_text(encrypted_text, cipher):
        """Desencripta texto usando Fernet"""
        if cipher:
            return cipher.decrypt(encrypted_text.encode()).decode()
        return encrypted_text

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Gestor de Contraseñas Seguras")
        self.root.geometry("900x650")
        
        self.bg_color = "#f5f6fa"
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.success_color = "#27ae60"
        self.warning_color = "#e74c3c"
        
        self.root.configure(bg=self.bg_color)
        
        self.db = Database()
        self.security = Security()
        self.current_user = None
        
        self.show_welcome_screen()
    
    def clear_window(self):
        """Limpia todos los widgets de la ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_welcome_screen(self):
        """Pantalla de bienvenida"""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        title_label = tk.Label(main_frame,
                              text="🔐 GESTOR DE CONTRASEÑAS",
                              font=("Arial", 28, "bold"),
                              bg=self.bg_color,
                              fg=self.primary_color)
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(main_frame,
                                 text="Almacena y protege todas tus contraseñas",
                                 font=("Arial", 14),
                                 bg=self.bg_color,
                                 fg="#7f8c8d")
        subtitle_label.pack(pady=(0, 50))
        
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(pady=30)
        
        login_btn = tk.Button(button_frame,
                             text="🚪 INICIAR SESIÓN",
                             font=("Arial", 12, "bold"),
                             bg=self.secondary_color,
                             fg="white",
                             width=25,
                             height=2,
                             command=self.show_login_screen)
        login_btn.pack(pady=10)
        
        register_btn = tk.Button(button_frame,
                                text="📝 REGISTRAR USUARIO",
                                font=("Arial", 12, "bold"),
                                bg=self.success_color,
                                fg="white",
                                width=25,
                                height=2,
                                command=self.show_register_screen)
        register_btn.pack(pady=10)
        
        if self.db.connection and self.db.connection.is_connected():
            status_text = "✅ Conectado a MySQL"
            status_color = self.success_color
        else:
            status_text = "❌ No conectado a MySQL"
            status_color = self.warning_color
        
        status_label = tk.Label(main_frame,
                               text=status_text,
                               font=("Arial", 10),
                               bg=self.bg_color,
                               fg=status_color)
        status_label.pack(pady=20)
    
    def show_login_screen(self):
        """Pantalla de inicio de sesión"""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill='both', padx=100, pady=50)
        
        tk.Label(main_frame,
                text="INICIAR SESIÓN",
                font=("Arial", 24, "bold"),
                bg=self.bg_color,
                fg=self.primary_color).pack(pady=(0, 40))

        form_frame = tk.Frame(main_frame, bg=self.bg_color)
        form_frame.pack(pady=20)
        
        # Usuario
        tk.Label(form_frame,
                text="Usuario:",
                font=("Arial", 12),
                bg=self.bg_color).grid(row=0, column=0, pady=15, sticky='e')
        
        self.login_user_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.login_user_entry.grid(row=0, column=1, padx=15, pady=15)
        
        # Contraseña
        tk.Label(form_frame,
                text="Contraseña:",
                font=("Arial", 12),
                bg=self.bg_color).grid(row=1, column=0, pady=15, sticky='e')
        
        self.login_pass_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, show="•")
        self.login_pass_entry.grid(row=1, column=1, padx=15, pady=15)
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(pady=40)
        
        tk.Button(btn_frame,
                 text="🔓 INICIAR SESIÓN",
                 font=("Arial", 11, "bold"),
                 bg=self.secondary_color,
                 fg="white",
                 padx=30,
                 pady=10,
                 command=self.login).pack(side='left', padx=10)
        
        tk.Button(btn_frame,
                 text="🔙 VOLVER",
                 font=("Arial", 11),
                 bg="#95a5a6",
                 fg="white",
                 padx=30,
                 pady=10,
                 command=self.show_welcome_screen).pack(side='left', padx=10)
    
    def show_register_screen(self):
        """Pantalla de registro de usuario - VERSIÓN CORREGIDA"""
        self.clear_window()
        
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(expand=True, fill='both', padx=100, pady=30)
        
        # Título
        tk.Label(main_frame,
                text="REGISTRAR NUEVO USUARIO",
                font=("Arial", 24, "bold"),
                bg=self.bg_color,
                fg=self.primary_color).pack(pady=(0, 30))
        
        # Formulario
        form_frame = tk.Frame(main_frame, bg=self.bg_color)
        form_frame.pack(pady=10)
        
        # Usuario
        tk.Label(form_frame,
                text="Usuario:",
                font=("Arial", 11),
                bg=self.bg_color).grid(row=0, column=0, pady=10, sticky='e')
        
        self.reg_user_entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
        self.reg_user_entry.grid(row=0, column=1, padx=15, pady=10)
        
        # Contraseña
        tk.Label(form_frame,
                text="Contraseña:",
                font=("Arial", 11),
                bg=self.bg_color).grid(row=1, column=0, pady=10, sticky='e')
        
        self.reg_pass_entry = tk.Entry(form_frame, font=("Arial", 11), width=30, show="•")
        self.reg_pass_entry.grid(row=1, column=1, padx=15, pady=10)
        
        # Confirmar Contraseña
        tk.Label(form_frame,
                text="Confirmar:",
                font=("Arial", 11),
                bg=self.bg_color).grid(row=2, column=0, pady=10, sticky='e')
        
        self.reg_confirm_entry = tk.Entry(form_frame, font=("Arial", 11), width=30, show="•")
        self.reg_confirm_entry.grid(row=2, column=1, padx=15, pady=10)
        
        # Indicador de fortaleza
        self.strength_label = tk.Label(form_frame,
                                      text="Fortaleza: ---",
                                      font=("Arial", 10),
                                      bg=self.bg_color,
                                      fg="black")
        self.strength_label.grid(row=3, column=1, pady=5, sticky='w')
        
        # Botón generar contraseña
        tk.Button(form_frame,
                 text="🔧 GENERAR CONTRASEÑA FUERTE",
                 font=("Arial", 9),
                 bg="#9b59b6",
                 fg="white",
                 command=self.generate_register_password).grid(row=4, column=1, pady=10, sticky='w')
        
        # Botones
        btn_frame = tk.Frame(main_frame, bg=self.bg_color)
        btn_frame.pack(pady=30)
        
        tk.Button(btn_frame,
                 text="✅ REGISTRAR",
                 font=("Arial", 11, "bold"),
                 bg=self.success_color,
                 fg="white",
                 padx=30,
                 pady=10,
                 command=self.register_user).pack(side='left', padx=10)
        
        tk.Button(btn_frame,
                 text="🔙 VOLVER",
                 font=("Arial", 11),
                 bg="#95a5a6",
                 fg="white",
                 padx=30,
                 pady=10,
                 command=self.show_welcome_screen).pack(side='left', padx=10)
        
        self.reg_pass_entry.bind('<KeyRelease>', self.update_strength_display)
    
    def update_strength_display(self, event=None):
        """Actualiza el indicador de fortaleza"""
        password = self.reg_pass_entry.get()
        if password:
            strength_info = self.security.check_password_strength(password)
            self.strength_label.config(
                text=f"Fortaleza: {strength_info['strength']}",
                fg=strength_info['color']
            )
        else:
            self.strength_label.config(text="Fortaleza: ---", fg="black")
    
    def generate_register_password(self):
        """Genera una contraseña fuerte para registro"""
        strong_pass = self.security.generate_strong_password(12)
        self.reg_pass_entry.delete(0, tk.END)
        self.reg_pass_entry.insert(0, strong_pass)
        self.reg_confirm_entry.delete(0, tk.END)
        self.reg_confirm_entry.insert(0, strong_pass)
        self.update_strength_display()
    
    def login(self):
        """Inicia sesión con usuario y contraseña"""
        usuario = self.login_user_entry.get()
        contrasena = self.login_pass_entry.get()
        
        if not usuario or not contrasena:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos")
            return
        
        try:
            # Buscar usuario en la base de datos
            result = self.db.execute_query(
                "SELECT id, usuario, contrasena_hash FROM usuarios WHERE usuario = %s",
                (usuario,),
                fetch=True
            )
            
            if result:
                hash_guardado = result[0]['contrasena_hash']
                
                # Verificar contraseña
                if self.security.verify_password(hash_guardado, contrasena):
                    self.current_user = {
                        'id': result[0]['id'],
                        'usuario': result[0]['usuario']
                    }
                    messagebox.showinfo("Éxito", f"¡Bienvenido, {usuario}!")
                    self.show_main_dashboard()
                else:
                    messagebox.showerror("Error", "Contraseña incorrecta")
            else:
                messagebox.showerror("Error", "Usuario no encontrado")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {str(e)}")
    
    def register_user(self):
        """Registra un nuevo usuario en el sistema"""
        usuario = self.reg_user_entry.get()
        contrasena = self.reg_pass_entry.get()
        confirmar = self.reg_confirm_entry.get()
        
        # Validaciones básicas
        if not usuario or not contrasena or not confirmar:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos")
            return
        
        if contrasena != confirmar:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        # Verificar fortaleza
        strength = self.security.check_password_strength(contrasena)
        if strength['score'] < 3:
            resp = messagebox.askyesno(
                "Contraseña débil",
                f"Tu contraseña es {strength['strength'].lower()}.\n"
                f"¿Deseas continuar de todos modos?"
            )
            if not resp:
                return
        
        try:
            # Verificar si usuario ya existe
            check = self.db.execute_query(
                "SELECT id FROM usuarios WHERE usuario = %s",
                (usuario,),
                fetch=True
            )
            
            if check:
                messagebox.showerror("Error", "El usuario ya existe")
                return
            
            # Crear hash de contraseña
            hashed = self.security.hash_password(contrasena)
            if not hashed:
                messagebox.showerror("Error", "Error al crear hash de contraseña")
                return
            
            # Insertar usuario en la base de datos
            rows = self.db.execute_query(
                "INSERT INTO usuarios (usuario, contrasena_hash) VALUES (%s, %s)",
                (usuario, hashed)
            )
            
            if rows and rows > 0:
                messagebox.showinfo("Éxito", "Usuario registrado correctamente")
                self.show_login_screen()
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar: {str(e)}")
    
    def show_main_dashboard(self):
        """Pantalla principal después de iniciar sesión"""
        self.clear_window()
        
        # Configurar menú
        self.setup_menu()
        
        # Título superior
        header = tk.Frame(self.root, bg=self.primary_color, height=70)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header,
                text=f"👤 {self.current_user['usuario']} - Gestor de Contraseñas",
                font=("Arial", 18, "bold"),
                bg=self.primary_color,
                fg="white").pack(expand=True)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Panel izquierdo - Añadir contraseña
        left_panel = tk.LabelFrame(main_frame,
                                  text="➕ AÑADIR NUEVA CONTRASEÑA",
                                  font=("Arial", 12, "bold"),
                                  bg=self.bg_color,
                                  padx=20,
                                  pady=20)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Campos del formulario
        tk.Label(left_panel, text="Sitio Web/Aplicación:", bg=self.bg_color).pack(anchor='w', pady=(0, 5))
        self.site_entry = tk.Entry(left_panel, font=("Arial", 11), width=30)
        self.site_entry.pack(fill='x', pady=(0, 15))
        
        tk.Label(left_panel, text="Usuario/Email:", bg=self.bg_color).pack(anchor='w', pady=(0, 5))
        self.site_user_entry = tk.Entry(left_panel, font=("Arial", 11), width=30)
        self.site_user_entry.pack(fill='x', pady=(0, 15))
        
        tk.Label(left_panel, text="Contraseña:", bg=self.bg_color).pack(anchor='w', pady=(0, 5))
        self.site_pass_entry = tk.Entry(left_panel, font=("Arial", 11), width=30, show="•")
        self.site_pass_entry.pack(fill='x', pady=(0, 10))
        
        # Botón generar
        tk.Button(left_panel,
                 text="🎲 GENERAR CONTRASEÑA FUERTE",
                 bg="#9b59b6",
                 fg="white",
                 command=self.generate_site_password).pack(pady=(0, 20))
        
        # Botón guardar
        tk.Button(left_panel,
                 text="💾 GUARDAR CONTRASEÑA",
                 font=("Arial", 11, "bold"),
                 bg=self.success_color,
                 fg="white",
                 command=self.save_password).pack()
        
        # Panel derecho - Lista de contraseñas
        right_panel = tk.LabelFrame(main_frame,
                                   text="📋 CONTRASEÑAS ALMACENADAS",
                                   font=("Arial", 12, "bold"),
                                   bg=self.bg_color,
                                   padx=20,
                                   pady=20)
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Treeview para mostrar contraseñas
        columns = ("ID", "Sitio Web", "Usuario", "Fortaleza")
        self.passwords_tree = ttk.Treeview(right_panel, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.passwords_tree.heading(col, text=col)
            self.passwords_tree.column(col, width=100)
        
        self.passwords_tree.pack(fill='both', expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(right_panel, orient="vertical", command=self.passwords_tree.yview)
        self.passwords_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        
        # Botones de acciones
        actions_frame = tk.Frame(right_panel, bg=self.bg_color)
        actions_frame.pack(pady=10)
        
        tk.Button(actions_frame,
                 text="🔄 ACTUALIZAR",
                 bg=self.secondary_color,
                 fg="white",
                 command=self.load_passwords).pack(side='left', padx=5)
        
        tk.Button(actions_frame,
                 text="👁️ MOSTRAR",
                 bg="#f39c12",
                 fg="white",
                 command=self.show_selected_password).pack(side='left', padx=5)
        
        tk.Button(actions_frame,
                 text="🗑️ ELIMINAR",
                 bg=self.warning_color,
                 fg="white",
                 command=self.delete_selected_password).pack(side='left', padx=5)
        
        # Panel inferior - Alertas
        alert_panel = tk.LabelFrame(main_frame,
                                   text="⚠️ ALERTAS DE SEGURIDAD",
                                   font=("Arial", 12, "bold"),
                                   bg=self.bg_color,
                                   fg=self.warning_color,
                                   padx=20,
                                   pady=20)
        alert_panel.pack(fill='x', pady=(20, 0))
        
        self.alerts_text = scrolledtext.ScrolledText(alert_panel, height=4, font=("Arial", 10))
        self.alerts_text.pack(fill='x')
        self.alerts_text.insert(tk.END, "✅ Sistema listo\n")
        
        # Cargar datos iniciales
        self.load_passwords()
    
    def setup_menu(self):
        """Configura la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Cerrar Sesión", command=self.logout)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Herramientas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Verificar seguridad", command=self.verify_security)
        tools_menu.add_command(label="Generar reporte", command=self.generate_report)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Manual de uso", command=self.show_manual)
        help_menu.add_command(label="Acerca de", command=self.show_about)
    
    def generate_site_password(self):
        """Genera contraseña fuerte para sitio web"""
        strong_pass = self.security.generate_strong_password(14)
        self.site_pass_entry.delete(0, tk.END)
        self.site_pass_entry.insert(0, strong_pass)
    
    def save_password(self):
        """Guarda una nueva contraseña"""
        sitio = self.site_entry.get()
        usuario_sitio = self.site_user_entry.get()
        contrasena = self.site_pass_entry.get()
        
        if not sitio or not usuario_sitio or not contrasena:
            messagebox.showwarning("Campos vacíos", "Completa todos los campos")
            return
        
        # Encriptar contraseña
        encrypted = self.security.encrypt_text(contrasena, self.db.cipher)
        
        try:
            # Guardar en base de datos
            rows = self.db.execute_query(
                """INSERT INTO contrasenas_almacenadas 
                (usuario_id, sitio_web, usuario_sitio, contrasena_encriptada) 
                VALUES (%s, %s, %s, %s)""",
                (self.current_user['id'], sitio, usuario_sitio, encrypted)
            )
            
            if rows and rows > 0:
                # Limpiar campos
                self.site_entry.delete(0, tk.END)
                self.site_user_entry.delete(0, tk.END)
                self.site_pass_entry.delete(0, tk.END)
                
                messagebox.showinfo("Éxito", "Contraseña guardada correctamente")
                self.load_passwords()
            else:
                messagebox.showerror("Error", "No se pudo guardar la contraseña")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")
    
    def load_passwords(self):
        """Carga las contraseñas del usuario"""
        # Limpiar treeview
        for item in self.passwords_tree.get_children():
            self.passwords_tree.delete(item)
        
        try:
            passwords = self.db.execute_query(
                """SELECT id, sitio_web, usuario_sitio, contrasena_encriptada 
                FROM contrasenas_almacenadas 
                WHERE usuario_id = %s 
                ORDER BY sitio_web""",
                (self.current_user['id'],),
                fetch=True
            )
            
            if passwords:
                for pwd in passwords:
                    # Obtener fortaleza
                    try:
                        decrypted = self.security.decrypt_text(pwd['contrasena_encriptada'], self.db.cipher)
                        strength = self.security.check_password_strength(decrypted)
                        strength_text = strength['strength']
                    except:
                        strength_text = "Desconocida"
                    
                    self.passwords_tree.insert('', 'end', values=(
                        pwd['id'],
                        pwd['sitio_web'],
                        pwd['usuario_sitio'],
                        strength_text
                    ))
        except Exception as e:
            print(f"Error cargando contraseñas: {e}")
    
    def show_selected_password(self):
        """Muestra la contraseña seleccionada"""
        selection = self.passwords_tree.selection()
        if not selection:
            messagebox.showwarning("Selección", "Selecciona una contraseña primero")
            return
        
        item = self.passwords_tree.item(selection[0])
        pass_id = item['values'][0]
        
        try:
            result = self.db.execute_query(
                "SELECT contrasena_encriptada FROM contrasenas_almacenadas WHERE id = %s",
                (pass_id,),
                fetch=True
            )
            
            if result:
                decrypted = self.security.decrypt_text(
                    result[0]['contrasena_encriptada'], 
                    self.db.cipher
                )
                
                # Mostrar en ventana
                pass_window = tk.Toplevel(self.root)
                pass_window.title("Contraseña")
                pass_window.geometry("400x150")
                pass_window.configure(bg=self.bg_color)
                
                tk.Label(pass_window,
                        text="CONTRASEÑA:",
                        font=("Arial", 12, "bold"),
                        bg=self.bg_color).pack(pady=10)
                
                # Mostrar contraseña con opción de ocultar
                pass_var = tk.StringVar(value=decrypted)
                pass_entry = tk.Entry(pass_window, 
                                     textvariable=pass_var, 
                                     font=("Courier", 12),
                                     show="•",
                                     width=30,
                                     justify='center')
                pass_entry.pack(pady=10)
                
                # Checkbox para mostrar/ocultar
                show_var = tk.BooleanVar()
                
                def toggle_password():
                    if show_var.get():
                        pass_entry.config(show="")
                    else:
                        pass_entry.config(show="•")
                
                tk.Checkbutton(pass_window,
                              text="Mostrar contraseña",
                              variable=show_var,
                              command=toggle_password,
                              bg=self.bg_color).pack(pady=5)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo recuperar: {str(e)}")
    
    def delete_selected_password(self):
        """Elimina la contraseña seleccionada"""
        selection = self.passwords_tree.selection()
        if not selection:
            messagebox.showwarning("Selección", "Selecciona una contraseña primero")
            return
        
        item = self.passwords_tree.item(selection[0])
        pass_id = item['values'][0]
        sitio = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar contraseña de '{sitio}'?"):
            try:
                rows = self.db.execute_query(
                    "DELETE FROM contrasenas_almacenadas WHERE id = %s",
                    (pass_id,)
                )
                
                if rows and rows > 0:
                    messagebox.showinfo("Éxito", "Contraseña eliminada")
                    self.load_passwords()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar")
                    
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")
    
    def verify_security(self):
        """Verifica la seguridad de las contraseñas"""
        try:
            passwords = self.db.execute_query(
                """SELECT sitio_web, contrasena_encriptada 
                FROM contrasenas_almacenadas 
                WHERE usuario_id = %s""",
                (self.current_user['id'],),
                fetch=True
            )
            
            if not passwords:
                messagebox.showinfo("Información", "No tienes contraseñas almacenadas")
                return
            
            weak = 0
            moderate = 0
            strong = 0
            
            for pwd in passwords:
                try:
                    decrypted = self.security.decrypt_text(pwd['contrasena_encriptada'], self.db.cipher)
                    strength = self.security.check_password_strength(decrypted)
                    
                    if strength['strength'] == "Débil":
                        weak += 1
                    elif strength['strength'] == "Moderada":
                        moderate += 1
                    else:
                        strong += 1
                except:
                    continue
            
            messagebox.showinfo(
                "Análisis de Seguridad",
                f"📊 RESULTADOS:\n\n"
                f"🔴 Débiles: {weak}\n"
                f"🟡 Moderadas: {moderate}\n"
                f"🟢 Fuertes: {strong}\n\n"
                f"Total: {weak + moderate + strong} contraseñas"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo analizar: {str(e)}")
    
    def generate_report(self):
        """Genera un reporte de contraseñas"""
        try:
            passwords = self.db.execute_query(
                """SELECT sitio_web, usuario_sitio, fecha_creacion 
                FROM contrasenas_almacenadas 
                WHERE usuario_id = %s""",
                (self.current_user['id'],),
                fetch=True
            )
            
            report = f"REPORTE DE CONTRASEÑAS\n"
            report += f"Usuario: {self.current_user['usuario']}\n"
            report += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            report += "="*50 + "\n\n"
            
            if passwords:
                for pwd in passwords:
                    report += f"Sitio: {pwd['sitio_web']}\n"
                    report += f"Usuario: {pwd['usuario_sitio']}\n"
                    report += f"Fecha: {pwd['fecha_creacion']}\n"
                    report += "-"*30 + "\n"
            else:
                report += "No hay contraseñas almacenadas\n"
            
            # Mostrar reporte
            report_window = tk.Toplevel(self.root)
            report_window.title("Reporte")
            report_window.geometry("500x400")
            
            text_area = scrolledtext.ScrolledText(report_window, wrap=tk.WORD)
            text_area.pack(fill='both', expand=True, padx=10, pady=10)
            text_area.insert(tk.END, report)
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar reporte: {str(e)}")
    
    def show_manual(self):
        """Muestra el manual de usuario"""
        manual = """MANUAL DE USUARIO

1. REGISTRO:
   • Crea un usuario único
   • Usa contraseña fuerte (mínimo 8 caracteres)

2. INICIO DE SESIÓN:
   • Usa tus credenciales registradas

3. GESTIÓN DE CONTRASEÑAS:
   • Añade nuevas contraseñas con sitio y usuario
   • Usa el generador de contraseñas
   • Visualiza y gestiona tus contraseñas

4. SEGURIDAD:
   • Todas las contraseñas están encriptadas
   • Se verifica la fortaleza automáticamente"""
        
        messagebox.showinfo("Manual de Usuario", manual)
    
    def show_about(self):
        """Muestra información sobre la aplicación"""
        about = """GESTOR DE CONTRASEÑAS SEGURAS
Versión 1.0

Características:
✅ Almacenamiento seguro
✅ Encriptación AES-256
✅ Verificación de fortaleza
✅ Generador de contraseñas
✅ Interfaz intuitiva

© 2025 Rikenny Encarnacion. Todos los derechos reservados."""
        
        messagebox.showinfo("Acerca de", about)
    
    def logout(self):
        """Cierra sesión y vuelve al inicio"""
        self.current_user = None
        self.show_welcome_screen()

# =================== EJECUCIÓN ===================
if __name__ == "__main__":
    # Crear ventana principal
    root = tk.Tk()
    
    # Centrar ventana
    window_width = 900
    window_height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    # Crear aplicación
    app = PasswordManagerApp(root)
    
    # Ejecutar
    root.mainloop()