-- 1. Crear base de datos
CREATE DATABASE IF NOT EXISTS gestor_contrasenas;
USE gestor_contrasenas;

-- 2. Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    usuario VARCHAR(50) UNIQUE NOT NULL, 
    contrasena_hash VARCHAR(255) NOT NULL, 
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla de contraseñas almacenadas
CREATE TABLE IF NOT EXISTS contrasenas_almacenadas (
    id INT AUTO_INCREMENT PRIMARY KEY, 
    usuario_id INT, 
    sitio_web VARCHAR(100) NOT NULL, 
    usuario_sitio VARCHAR(100) NOT NULL, 
    contrasena_encriptada TEXT NOT NULL, 
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- 4. Tabla de claves de cifrado
CREATE TABLE IF NOT EXISTS claves_cifrado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clave VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Tabla de alertas
CREATE TABLE IF NOT EXISTS alertas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    mensaje TEXT NOT NULL,
    tipo VARCHAR(20) DEFAULT 'advertencia',
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);