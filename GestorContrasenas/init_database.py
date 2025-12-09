from database import DatabaseConnection

def create_database():
    """Crea la base de datos y tablas si no existen"""
    db = DatabaseConnection()
    
    print("🛠️ Creando estructura de base de datos...")
    
    # Lista de tablas a crear
    tables_sql = [
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario VARCHAR(50) UNIQUE NOT NULL,
            contrasena_hash VARCHAR(255) NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS contrasenas_almacenadas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT,
            sitio_web VARCHAR(100) NOT NULL,
            usuario_sitio VARCHAR(100) NOT NULL,
            contrasena_encriptada TEXT NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS claves_cifrado (
            id INT AUTO_INCREMENT PRIMARY KEY,
            clave VARCHAR(255) NOT NULL,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS alertas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario_id INT,
            mensaje TEXT NOT NULL,
            tipo VARCHAR(20) DEFAULT 'advertencia',
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
        """
    ]
    
    # Ejecutar creación de tablas
    for i, sql in enumerate(tables_sql, 1):
        try:
            db.execute_query(sql)
            print(f"✅ Tabla {i} creada/verificada")
        except Exception as e:
            print(f"❌ Error creando tabla {i}: {e}")
    
    print("\n🎉 Base de datos inicializada correctamente")
    
    # Mostrar estado final
    tables = db.get_tables()
    print(f"\n📋 Total tablas: {len(tables)}")
    for table in tables:
        # Mostrar número de registros
        count_result = db.execute_query(f"SELECT COUNT(*) as count FROM {table}", fetch=True)
        if count_result:
            print(f"   • {table}: {count_result[0]['count']} registros")
    
    db.close()

if __name__ == "__main__":
    create_database()