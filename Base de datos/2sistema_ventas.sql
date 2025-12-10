DROP DATABASE IF EXISTS ventas;
CREATE DATABASE ventas;
USE ventas;

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    direccion TEXT,
    fecha_registro DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(50),
    precio DECIMAL(8,2) NOT NULL,
    stock INT DEFAULT 0,
    fecha_creacion DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE facturas (
    id_factura INT AUTO_INCREMENT PRIMARY KEY,
    numero_factura VARCHAR(20) UNIQUE NOT NULL,
    id_cliente INT NOT NULL,
    fecha DATE DEFAULT (CURRENT_DATE),
    subtotal DECIMAL(10,2),
    iva DECIMAL(10,2),
    total DECIMAL(10,2),
    estado ENUM('Pendiente', 'Pagada', 'Cancelada') DEFAULT 'Pendiente',
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
    ON DELETE CASCADE
);

CREATE TABLE detalle_factura (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_factura INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(8,2),
    subtotal DECIMAL(10,2),
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura)
    ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
    ON DELETE CASCADE
);

INSERT INTO clientes (cedula, nombre, apellido, telefono, email, direccion) VALUES
('001-1234567-8', 'Carlos', 'Mendoza', '809-111-2233', 'carlos@email.com', 'Calle 1 #101'),
('002-2345678-9', 'Ana', 'Gutiérrez', '809-222-3344', 'ana@email.com', 'Calle 2 #202'),
('003-3456789-0', 'Luis', 'Ramírez', '809-333-4455', 'luis@email.com', 'Calle 3 #303'),
('004-4567890-1', 'María', 'Sánchez', '809-444-5566', 'maria@email.com', 'Calle 4 #404');

INSERT INTO productos (codigo, nombre, descripcion, categoria, precio, stock) VALUES
('PROD-001', 'Laptop Dell XPS', 'Laptop 15 pulgadas, 16GB RAM, 512GB SSD', 'Tecnología', 1200.00, 15),
('PROD-002', 'Mouse Inalámbrico', 'Mouse óptico inalámbrico', 'Tecnología', 25.99, 50),
('PROD-003', 'Teclado Mecánico', 'Teclado gaming mecánico RGB', 'Tecnología', 89.99, 30),
('PROD-004', 'Monitor 24"', 'Monitor Full HD 24 pulgadas', 'Tecnología', 199.99, 20),
('PROD-005', 'Silla Ergonómica', 'Silla de oficina ergonómica', 'Muebles', 299.99, 10),
('PROD-006', 'Escritorio Ejecutivo', 'Escritorio de madera 150x80cm', 'Muebles', 450.00, 8);

INSERT INTO facturas (numero_factura, id_cliente, fecha, subtotal, iva, total, estado) VALUES
('FACT-2024-001', 1, '2024-01-15', 1200.00, 216.00, 1416.00, 'Pagada'),
('FACT-2024-002', 2, '2024-01-16', 289.98, 52.20, 342.18, 'Pagada'),
('FACT-2024-003', 3, '2024-01-17', 749.98, 135.00, 884.98, 'Pendiente'),
('FACT-2024-004', 1, '2024-01-18', 450.00, 81.00, 531.00, 'Pagada');

INSERT INTO detalle_factura (id_factura, id_producto, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 1, 1200.00, 1200.00),
(2, 2, 2, 25.99, 51.98),
(2, 3, 1, 89.99, 89.99),
(2, 4, 1, 199.99, 199.99),
(3, 5, 1, 299.99, 299.99),
(3, 6, 1, 450.00, 450.00),
(4, 6, 1, 450.00, 450.00);

SELECT c.nombre, c.apellido, COUNT(f.id_factura) AS total_facturas, SUM(f.total) AS total_gastado
FROM clientes c
LEFT JOIN facturas f ON c.id_cliente = f.id_cliente
GROUP BY c.id_cliente
ORDER BY total_gastado DESC;

SELECT p.nombre, p.categoria, p.precio, p.stock, SUM(df.cantidad) AS unidades_vendidas
FROM productos p
LEFT JOIN detalle_factura df ON p.id_producto = df.id_producto
GROUP BY p.id_producto
ORDER BY unidades_vendidas DESC;

SELECT f.numero_factura, c.nombre, c.apellido, f.fecha, f.total, f.estado
FROM facturas f
INNER JOIN clientes c ON f.id_cliente = c.id_cliente
WHERE f.estado = 'Pagada'
ORDER BY f.fecha DESC;

SELECT p.categoria, SUM(df.cantidad) AS total_vendido, SUM(df.subtotal) AS ingresos_totales
FROM productos p
INNER JOIN detalle_factura df ON p.id_producto = df.id_producto
GROUP BY p.categoria
ORDER BY ingresos_totales DESC;

SELECT f.numero_factura, f.fecha, p.nombre AS producto, df.cantidad, df.precio_unitario, df.subtotal
FROM facturas f
INNER JOIN detalle_factura df ON f.id_factura = df.id_factura
INNER JOIN productos p ON df.id_producto = p.id_producto
WHERE f.id_cliente = 1;