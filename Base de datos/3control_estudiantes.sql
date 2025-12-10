DROP DATABASE IF EXISTS colegio;
CREATE DATABASE colegio;
USE colegio;

CREATE TABLE estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    genero ENUM('M', 'F'),
    direccion TEXT,
    telefono VARCHAR(15),
    email VARCHAR(100),
    fecha_ingreso DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    codigo_curso VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    creditos INT DEFAULT 1,
    nivel VARCHAR(20),
    profesor VARCHAR(100),
    horario VARCHAR(50),
    aula VARCHAR(20),
    cupo_maximo INT DEFAULT 30
);

CREATE TABLE matriculas (
    id_matricula INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_curso INT NOT NULL,
    fecha_matricula DATE DEFAULT (CURRENT_DATE),
    periodo_academico VARCHAR(20),
    estado ENUM('Activa', 'Retirada', 'Finalizada') DEFAULT 'Activa',
    nota_final DECIMAL(4,2),
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante)
    ON DELETE CASCADE,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso)
    ON DELETE CASCADE,
    UNIQUE KEY unique_matricula (id_estudiante, id_curso, periodo_academico)
);

INSERT INTO estudiantes (matricula, nombre, apellido, fecha_nacimiento, genero, direccion, telefono, email) VALUES
('2024-001', 'Juan', 'Pérez', '2008-03-15', 'M', 'Calle Principal 123', '809-111-2222', 'juan@colegio.edu'),
('2024-002', 'María', 'González', '2009-05-22', 'F', 'Avenida Central 456', '809-222-3333', 'maria@colegio.edu'),
('2024-003', 'Carlos', 'Rodríguez', '2008-11-10', 'M', 'Sector Norte 789', '809-333-4444', 'carlos@colegio.edu'),
('2024-004', 'Ana', 'Martínez', '2009-07-30', 'F', 'Residencial Este 101', '809-444-5555', 'ana@colegio.edu'),
('2024-005', 'Luis', 'Hernández', '2008-01-25', 'M', 'Urbanización Sur 202', '809-555-6666', 'luis@colegio.edu');

INSERT INTO cursos (codigo_curso, nombre, descripcion, creditos, nivel, profesor, horario, aula, cupo_maximo) VALUES
('MAT-101', 'Matemáticas Básicas', 'Álgebra y aritmética fundamental', 4, 'Básico', 'Prof. Sánchez', 'Lunes 8:00-10:00', 'Aula 101', 25),
('ESP-101', 'Español', 'Gramática y literatura', 3, 'Básico', 'Prof. Díaz', 'Martes 10:00-12:00', 'Aula 102', 25),
('ING-101', 'Inglés Básico', 'Inglés nivel principiante', 3, 'Básico', 'Prof. Johnson', 'Miércoles 8:00-10:00', 'Aula 103', 20),
('CSC-101', 'Informática', 'Introducción a la computación', 2, 'Básico', 'Prof. Ramírez', 'Jueves 14:00-16:00', 'Lab 1', 15),
('ART-101', 'Arte', 'Historia y apreciación del arte', 2, 'Básico', 'Prof. López', 'Viernes 10:00-12:00', 'Aula 201', 30);

INSERT INTO matriculas (id_estudiante, id_curso, fecha_matricula, periodo_academico, estado, nota_final) VALUES
(1, 1, '2024-01-10', '2024-1', 'Activa', NULL),
(1, 2, '2024-01-10', '2024-1', 'Activa', NULL),
(1, 3, '2024-01-10', '2024-1', 'Activa', NULL),
(2, 1, '2024-01-11', '2024-1', 'Activa', NULL),
(2, 4, '2024-01-11', '2024-1', 'Activa', NULL),
(3, 2, '2024-01-12', '2024-1', 'Activa', NULL),
(3, 3, '2024-01-12', '2024-1', 'Activa', NULL),
(3, 5, '2024-01-12', '2024-1', 'Activa', NULL),
(4, 1, '2024-01-13', '2024-1', 'Activa', NULL),
(4, 5, '2024-01-13', '2024-1', 'Activa', NULL),
(5, 4, '2024-01-14', '2024-1', 'Activa', NULL),
(5, 5, '2024-01-14', '2024-1', 'Activa', NULL);

UPDATE matriculas SET nota_final = 85.5 WHERE id_matricula = 1;
UPDATE matriculas SET nota_final = 92.0 WHERE id_matricula = 2;
UPDATE matriculas SET nota_final = 78.5 WHERE id_matricula = 3;
UPDATE matriculas SET nota_final = 88.0 WHERE id_matricula = 4;
UPDATE matriculas SET nota_final = 95.5 WHERE id_matricula = 5;

SELECT e.matricula, CONCAT(e.nombre, ' ', e.apellido) AS estudiante, 
       TIMESTAMPDIFF(YEAR, e.fecha_nacimiento, CURDATE()) AS edad,
       e.genero, COUNT(m.id_curso) AS cursos_inscritos
FROM estudiantes e
LEFT JOIN matriculas m ON e.id_estudiante = m.id_estudiante AND m.estado = 'Activa'
GROUP BY e.id_estudiante
ORDER BY edad;

SELECT c.nombre AS curso, c.profesor, c.horario, c.aula, 
       COUNT(m.id_estudiante) AS estudiantes_inscritos,
       c.cupo_maximo
FROM cursos c
LEFT JOIN matriculas m ON c.id_curso = m.id_curso AND m.estado = 'Activa'
GROUP BY c.id_curso
ORDER BY estudiantes_inscritos DESC;

SELECT CONCAT(e.nombre, ' ', e.apellido) AS estudiante,
       c.nombre AS curso,
       m.nota_final,
       CASE 
           WHEN m.nota_final >= 90 THEN 'Excelente'
           WHEN m.nota_final >= 80 THEN 'Bueno'
           WHEN m.nota_final >= 70 THEN 'Regular'
           ELSE 'Necesita mejorar'
       END AS categoria
FROM matriculas m
INNER JOIN estudiantes e ON m.id_estudiante = e.id_estudiante
INNER JOIN cursos c ON m.id_curso = c.id_curso
WHERE m.nota_final IS NOT NULL
ORDER BY m.nota_final DESC;

SELECT c.nombre AS curso, 
       AVG(m.nota_final) AS promedio_notas,
       MIN(m.nota_final) AS nota_minima,
       MAX(m.nota_final) AS nota_maxima,
       COUNT(m.id_matricula) AS total_estudiantes
FROM cursos c
INNER JOIN matriculas m ON c.id_curso = m.id_curso
WHERE m.nota_final IS NOT NULL
GROUP BY c.id_curso
ORDER BY promedio_notas DESC;

SELECT e.matricula, CONCAT(e.nombre, ' ', e.apellido) AS estudiante,
       GROUP_CONCAT(c.nombre SEPARATOR ', ') AS cursos_inscritos
FROM estudiantes e
INNER JOIN matriculas m ON e.id_estudiante = m.id_estudiante
INNER JOIN cursos c ON m.id_curso = c.id_curso
WHERE m.estado = 'Activa'
GROUP BY e.id_estudiante
ORDER BY e.apellido;