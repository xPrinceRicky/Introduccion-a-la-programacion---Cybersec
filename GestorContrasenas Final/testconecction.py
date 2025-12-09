from database import DatabaseConnection

def main():
    print("Probando conexión a MySQL...")
    
    # Crear instancia de conexión
    db = DatabaseConnection()
    
    # Probar conexión
    if db.test_connection():
        print("¡Conexión exitosa!")
        
        # Mostrar tablas existentes
        tables = db.get_tables()
        if tables:
            print("\nTablas en la base de datos:")
            for table in tables:
                print(f"   • {table}")
        else:
            print("\nNo hay tablas. Ejecuta el script de creación.")
    else:
        print("No se pudo conectar a MySQL")
    
    db.close()

if __name__ == "__main__":
    main()