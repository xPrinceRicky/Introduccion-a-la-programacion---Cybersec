DROP DATABASE IF EXISTS gestion_academica;
CREATE DATABASE gestion_academica;
USE gestion_academica;

CREATE TABLE Departamento (
    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100),
    presupuesto DECIMAL(10,2),
    fecha_creacion DATE
);

CREATE TABLE Estudiante (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    email VARCHAR(100) UNIQUE,
    telefono VARCHAR(15),
    direccion TEXT,
    fecha_ingreso DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE Profesor (
    id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    salario DECIMAL(8,2),
    fecha_contratacion DATE,
    id_departamento INT,
    FOREIGN KEY (id_departamento) REFERENCES Departamento(id_departamento)
    ON DELETE SET NULL
);

CREATE TABLE Curso (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    codigo_curso VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    creditos INT DEFAULT 3,
    horas_semanales INT,
    prerequisito TEXT,
    id_profesor INT,
    FOREIGN KEY (id_profesor) REFERENCES Profesor(id_profesor)
    ON DELETE SET NULL
);

CREATE TABLE Clase (
    id_clase INT AUTO_INCREMENT PRIMARY KEY,
    id_curso INT NOT NULL,
    fecha_clase DATE NOT NULL,
    hora_inicio TIME,
    hora_fin TIME,
    aula VARCHAR(20),
    tema VARCHAR(200),
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso)
    ON DELETE CASCADE
);

CREATE TABLE Inscripcion (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_curso INT NOT NULL,
    fecha_inscripcion DATE DEFAULT (CURRENT_DATE),
    semestre VARCHAR(20),
    estado ENUM('Activa', 'Cancelada', 'Finalizada') DEFAULT 'Activa',
    UNIQUE KEY unique_inscripcion (id_estudiante, id_curso, semestre),
    FOREIGN KEY (id_estudiante) REFERENCES Estudiante(id_estudiante)
    ON DELETE CASCADE,
    FOREIGN KEY (id_curso) REFERENCES Curso(id_curso)
    ON DELETE CASCADE
);

CREATE TABLE Calificacion (
    id_calificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_inscripcion INT NOT NULL,
    tipo_evaluacion VARCHAR(50),
    puntaje DECIMAL(5,2) CHECK (puntaje >= 0 AND puntaje <= 100),
    fecha_evaluacion DATE DEFAULT (CURRENT_DATE),
    comentario TEXT,
    FOREIGN KEY (id_inscripcion) REFERENCES Inscripcion(id_inscripcion)
    ON DELETE CASCADE
);

INSERT INTO Departamento (nombre, ubicacion, presupuesto, fecha_creacion) VALUES
('Ciencias de la Computación', 'Edificio A, Piso 3', 50000.00, '2010-08-15'),
('Matemáticas', 'Edificio B, Piso 2', 35000.00, '2008-05-20'),
('Ingeniería', 'Edificio C, Piso 1', 75000.00, '2012-03-10');

INSERT INTO Estudiante (cedula, nombre, apellido, fecha_nacimiento, email, telefono, direccion, fecha_ingreso) VALUES
('001-1234567-8', 'Juan', 'Pérez', '2000-05-15', 'juan.perez@email.com', '809-123-4567', 'Calle Principal #123', '2022-08-20'),
('002-2345678-9', 'María', 'González', '2001-02-28', 'maria.gonzalez@email.com', '809-234-5678', 'Avenida Central #456', '2022-08-20'),
('003-3456789-0', 'Carlos', 'Rodríguez', '1999-11-10', 'carlos.rodriguez@email.com', '809-345-6789', 'Sector Norte #789', '2021-08-15'),
('004-4567890-1', 'Ana', 'Martínez', '2002-07-22', 'ana.martinez@email.com', '809-456-7890', 'Residencial Este #101', '2023-01-10');

INSERT INTO Profesor (cedula, nombre, apellido, especialidad, email, salario, fecha_contratacion, id_departamento) VALUES
('101-9876543-2', 'Roberto', 'Sánchez', 'Inteligencia Artificial', 'roberto.sanchez@uni.edu', 75000.00, '2015-06-01', 1),
('102-8765432-1', 'Laura', 'Díaz', 'Análisis Numérico', 'laura.diaz@uni.edu', 68000.00, '2018-03-15', 2),
('103-7654321-0', 'Miguel', 'Hernández', 'Bases de Datos', 'miguel.hernandez@uni.edu', 72000.00, '2016-09-10', 1),
('104-6543210-9', 'Elena', 'Castillo', 'Estructuras Discretas', 'elena.castillo@uni.edu', 65000.00, '2020-01-20', 3);

INSERT INTO Curso (codigo_curso, nombre, descripcion, creditos, horas_semanales, prerequisito, id_profesor) VALUES
('CC101', 'Introducción a la Programación', 'Fundamentos de programación usando Python', 4, 6, 'Ninguno', 1),
('CC201', 'Bases de Datos I', 'Diseño e implementación de bases de datos relacionales', 4, 6, 'CC101', 3),
('MAT101', 'Cálculo I', 'Cálculo diferencial e integral', 4, 5, 'Ninguno', 2),
('CC301', 'Inteligencia Artificial', 'Introducción a técnicas de IA', 3, 4, 'CC201', 1),
('ING101', 'Estructuras Discretas', 'Matemáticas discretas para ingeniería', 3, 4, 'Ninguno', 4);

INSERT INTO Clase (id_curso, fecha_clase, hora_inicio, hora_fin, aula, tema) VALUES
(1, '2024-01-10', '08:00:00', '10:00:00', 'Aula 301', 'Introducción a Python'),
(1, '2024-01-12', '08:00:00', '10:00:00', 'Aula 301', 'Variables y tipos de datos'),
(2, '2024-01-11', '10:00:00', '12:00:00', 'Aula 302', 'Modelo Entidad-Relación'),
(3, '2024-01-15', '14:00:00', '17:00:00', 'Aula 201', 'Límites y continuidad'),
(4, '2024-01-16', '09:00:00', '11:00:00', 'Lab 101', 'Introducción a algoritmos de búsqueda');

INSERT INTO Inscripcion (id_estudiante, id_curso, fecha_inscripcion, semestre, estado) VALUES
(1, 1, '2024-01-05', '2024-1', 'Activa'),
(1, 2, '2024-01-05', '2024-1', 'Activa'),
(2, 1, '2024-01-06', '2024-1', 'Activa'),
(2, 3, '2024-01-06', '2024-1', 'Activa'),
(3, 2, '2024-01-07', '2024-1', 'Activa'),
(3, 4, '2024-01-07', '2024-1', 'Activa'),
(4, 1, '2024-01-08', '2024-1', 'Activa'),
(4, 5, '2024-01-08', '2024-1', 'Activa');

INSERT INTO Calificacion (id_inscripcion, tipo_evaluacion, puntaje, fecha_evaluacion, comentario) VALUES
(1, 'Quiz 1', 85.5, '2024-01-20', 'Buen desempeño'),
(1, 'Tarea 1', 90.0, '2024-01-25', 'Excelente trabajo'),
(2, 'Examen Parcial', 78.0, '2024-02-10', 'Necesita mejorar en consultas complejas'),
(3, 'Quiz 1', 92.5, '2024-01-20', 'Muy buen desempeño'),
(4, 'Proyecto', 88.0, '2024-02-15', 'Proyecto bien estructurado'),
(5, 'Examen Final', 95.0, '2024-03-20', 'Excelente comprensión del tema'),
(6, 'Tarea 2', 82.5, '2024-02-05', 'Buen trabajo');

#Consulta estudiantes por cursos y calificaciones
SELECT 
    e.cedula,
    CONCAT(e.nombre, ' ', e.apellido) AS estudiante,
    c.nombre AS curso,
    ca.tipo_evaluacion,
    ca.puntaje,
    CASE 
        WHEN ca.puntaje >= 90 THEN 'Excelente'
        WHEN ca.puntaje >= 80 THEN 'Bueno'
        WHEN ca.puntaje >= 70 THEN 'Regular'
        ELSE 'Necesita mejorar'
    END AS categoria
FROM Estudiante e
INNER JOIN Inscripcion i ON e.id_estudiante = i.id_estudiante
INNER JOIN Curso c ON i.id_curso = c.id_curso
INNER JOIN Calificacion ca ON i.id_inscripcion = ca.id_inscripcion
WHERE i.estado = 'Activa'
ORDER BY e.apellido, c.nombre;

#Consulta estadisticas de departamentos
SELECT 
    d.nombre AS departamento,
    COUNT(p.id_profesor) AS total_profesores,
    ROUND(AVG(p.salario), 2) AS salario_promedio,
    COUNT(DISTINCT c.id_curso) AS total_cursos
FROM Departamento d
LEFT JOIN Profesor p ON d.id_departamento = p.id_departamento
LEFT JOIN Curso c ON p.id_profesor = c.id_profesor
GROUP BY d.id_departamento
ORDER BY total_profesores DESC;

