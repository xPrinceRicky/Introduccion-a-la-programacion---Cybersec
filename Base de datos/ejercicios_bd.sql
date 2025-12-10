DROP DATABASE IF EXISTS biblioteca;
CREATE DATABASE biblioteca;
USE biblioteca;

CREATE TABLE autores (
    id_autor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(50),
    fecha_nacimiento DATE,
    fecha_defuncion DATE,
    email VARCHAR(100),
    UNIQUE KEY unique_autor (nombre, apellido)
);

CREATE TABLE libros (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    titulo VARCHAR(200) NOT NULL,
    genero VARCHAR(50),
    anio_publicacion INT,
    editorial VARCHAR(100),
    num_paginas INT,
    precio DECIMAL(6,2),
    stock INT DEFAULT 1,
    id_autor INT NOT NULL,
    FOREIGN KEY (id_autor) REFERENCES autores(id_autor)
    ON DELETE CASCADE
);

INSERT INTO autores (nombre, apellido, nacionalidad, fecha_nacimiento, fecha_defuncion, email) VALUES
('Gabriel', 'García Márquez', 'Colombiano', '1927-03-06', '2014-04-17', NULL),
('Isabel', 'Allende', 'Chilena', '1942-08-02', NULL, 'isabel@allende.com'),
('Mario', 'Vargas Llosa', 'Peruano', '1936-03-28', NULL, NULL),
('Julio', 'Cortázar', 'Argentino', '1914-08-26', '1984-02-12', NULL),
('Laura', 'Esquivel', 'Mexicana', '1950-09-30', NULL, 'laura@esquivel.com');

INSERT INTO libros (isbn, titulo, genero, anio_publicacion, editorial, num_paginas, precio, stock, id_autor) VALUES
('978-843-760-494-7', 'Cien años de soledad', 'Realismo mágico', 1967, 'Sudamericana', 471, 25.99, 10, 1),
('978-956-239-227-6', 'La casa de los espíritus', 'Realismo mágico', 1982, 'Plaza & Janés', 499, 22.50, 8, 2),
('978-612-456-789-0', 'La ciudad y los perros', 'Novela', 1963, 'Seix Barral', 355, 19.99, 5, 3),
('978-987-113-807-1', 'Rayuela', 'Novela experimental', 1963, 'Sudamericana', 736, 28.75, 3, 4),
('978-968-190-541-8', 'Como agua para chocolate', 'Novela romántica', 1989, 'Planeta', 256, 17.50, 12, 5),
('978-843-760-682-8', 'El amor en los tiempos del cólera', 'Novela romántica', 1985, 'Sudamericana', 464, 21.99, 7, 1),
('978-956-239-843-8', 'Eva Luna', 'Novela', 1987, 'Plaza & Janés', 317, 20.50, 6, 2),
('978-612-457-123-4', 'La fiesta del chivo', 'Novela histórica', 2000, 'Alfaguara', 476, 24.99, 4, 3);

SELECT a.nombre, a.apellido, a.nacionalidad, COUNT(l.id_libro) AS total_libros
FROM autores a
LEFT JOIN libros l ON a.id_autor = l.id_autor
GROUP BY a.id_autor
ORDER BY total_libros DESC;

SELECT l.titulo, l.genero, l.anio_publicacion, CONCAT(a.nombre, ' ', a.apellido) AS autor
FROM libros l
INNER JOIN autores a ON l.id_autor = a.id_autor
WHERE l.stock > 0
ORDER BY l.anio_publicacion;

SELECT l.titulo, l.precio, l.stock, l.editorial
FROM libros l
WHERE l.precio BETWEEN 15 AND 25
ORDER BY l.precio DESC;

SELECT genero, COUNT(*) AS cantidad_libros, AVG(precio) AS precio_promedio
FROM libros
GROUP BY genero
ORDER BY cantidad_libros DESC;

SELECT CONCAT(nombre, ' ', apellido) AS autor_completo,
       nacionalidad,
       TIMESTAMPDIFF(YEAR, fecha_nacimiento, COALESCE(fecha_defuncion, CURDATE())) AS edad
FROM autores
WHERE fecha_defuncion IS NULL;