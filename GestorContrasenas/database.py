import mysql.connector
from mysql.connector import Error
import config

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establece conexión con MySQL con manejo de errores"""
        try:
            config_data = config.DatabaseConfig.get_connection_string()
            self.connection = mysql.connector.connect(**config_data)
            
            if self.connection.is_connected():
                print("Conexión exitosa a MySQL")
                print(f"ase de datos: {config.DatabaseConfig.DATABASE}")
                print(f"Usuario: {config.DatabaseConfig.USER}")
                return True
                
        except Error as e:
            print(f"Error de conexión: {e}")
            self.show_connection_help()
            return False
    
    def show_connection_help(self):
        """Muestra ayuda para solucionar problemas de conexión"""
        print("\n" + "="*50)
        print("SOLUCIÓN DE PROBLEMAS DE CONEXIÓN")
        print("="*50)
        print("1. Verifica que MySQL esté ejecutándose:")
        print("   - Windows: Servicios → MySQL")
        print("   - XAMPP: Panel de Control → Start MySQL")
        print("\n2. Verifica credenciales en config.py:")
        print(f"   Host: {config.DatabaseConfig.HOST}")
        print(f"   Usuario: {config.DatabaseConfig.USER}")
        print(f"   Base de datos: {config.DatabaseConfig.DATABASE}")
        print("\n3. Prueba la conexión en MySQL Workbench")
        print("="*50)
    
    def execute_query(self, query, params=None, fetch=False):
        """Ejecuta una consulta SQL"""
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if fetch:
                if 'SELECT' in query.upper():
                    return cursor.fetchall()
                else:
                    self.connection.commit()
                    return cursor.lastrowid
            else:
                self.connection.commit()
                return cursor.rowcount
                
        except Error as e:
            print(f"Error en consulta: {e}")
            print(f"Consulta: {query}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def test_connection(self):
        """Prueba la conexión con una consulta simple"""
        try:
            result = self.execute_query("SELECT VERSION()", fetch=True)
            if result:
                print(f"MySQL Version: {result[0]['VERSION()']}")
                return True
        except:
            return False
    
    def get_tables(self):
        """Obtiene lista de tablas en la base de datos"""
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = %s
        """
        tables = self.execute_query(query, (config.DatabaseConfig.DATABASE,), fetch=True)
        return [table['table_name'] for table in tables] if tables else []
    
    def close(self):
        """Cierra la conexión"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada")