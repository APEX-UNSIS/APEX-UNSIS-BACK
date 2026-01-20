-- =====================================================
-- Script de inicialización de base de datos APEX-UNSIS
-- =====================================================
-- Este script crea todas las tablas y las llena con datos de ejemplo
-- Ejecutar en pgAdmin o psql después de crear la base de datos

-- =====================================================
-- ELIMINAR TABLAS SI EXISTEN (CUIDADO EN PRODUCCIÓN)
-- =====================================================
DROP TABLE IF EXISTS asignacion_sinodales CASCADE;
DROP TABLE IF EXISTS asignacion_aulas_y_aplicadores CASCADE;
DROP TABLE IF EXISTS grupos_por_solicitud_de_examen CASCADE;
DROP TABLE IF EXISTS solicitudes_de_examen CASCADE;
DROP TABLE IF EXISTS permisos_sinodales_por_materia CASCADE;
DROP TABLE IF EXISTS horarios_regulares_de_clase CASCADE;
DROP TABLE IF EXISTS ventanas_de_aplicacion_por_periodo CASCADE;
DROP TABLE IF EXISTS grupos_escolares CASCADE;
DROP TABLE IF EXISTS aulas CASCADE;
DROP TABLE IF EXISTS tipos_de_evaluacion CASCADE;
DROP TABLE IF EXISTS materias CASCADE;
DROP TABLE IF EXISTS periodos_academicos CASCADE;
DROP TABLE IF EXISTS usuarios CASCADE;
DROP TABLE IF EXISTS profesores CASCADE;
DROP TABLE IF EXISTS carreras CASCADE;

-- =====================================================
-- CREAR TABLAS
-- =====================================================

-- Tabla: carreras
CREATE TABLE carreras (
    id_carrera VARCHAR(20) PRIMARY KEY,
    nombre_carrera VARCHAR(100)
);

-- Tabla: usuarios
CREATE TABLE usuarios (
    id_usuario VARCHAR(50) PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    id_carrera VARCHAR(20),
    contraseña VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_usuario_carrera FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);

-- Tabla: profesores
CREATE TABLE profesores (
    id_profesor VARCHAR(20) PRIMARY KEY,
    nombre_profesor VARCHAR(60),
    is_disable BOOLEAN DEFAULT FALSE
);

-- Tabla: periodos_academicos
CREATE TABLE periodos_academicos (
    id_periodo VARCHAR(20) PRIMARY KEY,
    nombre_periodo VARCHAR(30)
);

-- Tabla: materias
CREATE TABLE materias (
    id_materia VARCHAR(20) PRIMARY KEY,
    nombre_materia VARCHAR(50)
);

-- Tabla: tipos_de_evaluacion
CREATE TABLE tipos_de_evaluacion (
    id_evaluacion VARCHAR(20) PRIMARY KEY,
    nombre_evaluacion VARCHAR(30)
);

-- Tabla: aulas
CREATE TABLE aulas (
    id_aula VARCHAR(20) PRIMARY KEY,
    nombre_aula VARCHAR(50),
    capacidad INTEGER,
    is_disable BOOLEAN DEFAULT FALSE
);

-- Tabla: grupos_escolares
CREATE TABLE grupos_escolares (
    id_grupo VARCHAR(20) PRIMARY KEY,
    nombre_grupo VARCHAR(20),
    numero_alumnos INTEGER,
    id_carrera VARCHAR(20),
    CONSTRAINT fk_grupo_carrera FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);

-- Tabla: ventanas_de_aplicacion_por_periodo
CREATE TABLE ventanas_de_aplicacion_por_periodo (
    id_ventana VARCHAR(20) PRIMARY KEY,
    id_periodo VARCHAR(20),
    id_evaluacion VARCHAR(20),
    fecha_inicio_examenes DATE,
    fecha_fin_examenes DATE,
    CONSTRAINT fk_ventana_periodo FOREIGN KEY (id_periodo) REFERENCES periodos_academicos(id_periodo),
    CONSTRAINT fk_ventana_evaluacion FOREIGN KEY (id_evaluacion) REFERENCES tipos_de_evaluacion(id_evaluacion)
);

-- Tabla: horarios_regulares_de_clase
CREATE TABLE horarios_regulares_de_clase (
    id_horario_clase VARCHAR(20) PRIMARY KEY,
    id_periodo VARCHAR(20),
    id_materia VARCHAR(20),
    id_grupo VARCHAR(20),
    id_profesor VARCHAR(20),
    id_aula VARCHAR(20),
    dia_semana INTEGER,
    hora_inicio TIME,
    hora_fin TIME,
    CONSTRAINT fk_horario_periodo FOREIGN KEY (id_periodo) REFERENCES periodos_academicos(id_periodo),
    CONSTRAINT fk_horario_materia FOREIGN KEY (id_materia) REFERENCES materias(id_materia),
    CONSTRAINT fk_horario_grupo FOREIGN KEY (id_grupo) REFERENCES grupos_escolares(id_grupo),
    CONSTRAINT fk_horario_profesor FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor),
    CONSTRAINT fk_horario_aula FOREIGN KEY (id_aula) REFERENCES aulas(id_aula)
);

-- Tabla: permisos_sinodales_por_materia
CREATE TABLE permisos_sinodales_por_materia (
    id_regla VARCHAR(20) PRIMARY KEY,
    id_profesor VARCHAR(20),
    id_materia VARCHAR(20),
    CONSTRAINT fk_permiso_profesor FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor),
    CONSTRAINT fk_permiso_materia FOREIGN KEY (id_materia) REFERENCES materias(id_materia)
);

-- Tabla: solicitudes_de_examen
CREATE TABLE solicitudes_de_examen (
    id_horario VARCHAR(20) PRIMARY KEY,
    id_periodo VARCHAR(20),
    id_evaluacion VARCHAR(20),
    id_materia VARCHAR(20),
    fecha_examen DATE,
    hora_inicio TIME,
    hora_fin TIME,
    estado INTEGER DEFAULT 0,
    motivo_rechazo VARCHAR(255),
    is_manualmente_editado BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_solicitud_periodo FOREIGN KEY (id_periodo) REFERENCES periodos_academicos(id_periodo),
    CONSTRAINT fk_solicitud_evaluacion FOREIGN KEY (id_evaluacion) REFERENCES tipos_de_evaluacion(id_evaluacion),
    CONSTRAINT fk_solicitud_materia FOREIGN KEY (id_materia) REFERENCES materias(id_materia)
);

-- Tabla: grupos_por_solicitud_de_examen
CREATE TABLE grupos_por_solicitud_de_examen (
    id_examen_grupo VARCHAR(20) PRIMARY KEY,
    id_horario VARCHAR(20),
    id_grupo VARCHAR(20),
    CONSTRAINT fk_examen_grupo_solicitud FOREIGN KEY (id_horario) REFERENCES solicitudes_de_examen(id_horario),
    CONSTRAINT fk_examen_grupo_grupo FOREIGN KEY (id_grupo) REFERENCES grupos_escolares(id_grupo)
);

-- Tabla: asignacion_aulas_y_aplicadores
CREATE TABLE asignacion_aulas_y_aplicadores (
    id_examen_aula VARCHAR(20) PRIMARY KEY,
    id_horario VARCHAR(20),
    id_aula VARCHAR(20),
    id_profesor_aplicador VARCHAR(20),
    CONSTRAINT fk_asignacion_aula_solicitud FOREIGN KEY (id_horario) REFERENCES solicitudes_de_examen(id_horario),
    CONSTRAINT fk_asignacion_aula_aula FOREIGN KEY (id_aula) REFERENCES aulas(id_aula),
    CONSTRAINT fk_asignacion_aula_profesor FOREIGN KEY (id_profesor_aplicador) REFERENCES profesores(id_profesor)
);

-- Tabla: asignacion_sinodales
CREATE TABLE asignacion_sinodales (
    id_examen_sinodal VARCHAR(20) PRIMARY KEY,
    id_horario VARCHAR(20),
    id_profesor VARCHAR(20),
    CONSTRAINT fk_asignacion_sinodal_solicitud FOREIGN KEY (id_horario) REFERENCES solicitudes_de_examen(id_horario),
    CONSTRAINT fk_asignacion_sinodal_profesor FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor)
);

-- =====================================================
-- INSERTAR DATOS DE EJEMPLO
-- =====================================================

-- Carreras
INSERT INTO carreras (id_carrera, nombre_carrera) VALUES
('ING-SIS', 'Ingeniería en Sistemas'),
('ING-IND', 'Ingeniería Industrial'),
('LIC-ADM', 'Licenciatura en Administración'),
('ING-CIV', 'Ingeniería Civil');

-- Usuarios (contraseñas hasheadas con bcrypt)
-- admin123 -> $2b$12$4dGtQjmlRcIhLzEED.G.sut2y34cw7rvHCIzp/CsYPKeT2VEIQ7AK
-- jefe123 -> $2b$12$EpTN7znyFdvpf6oCBwhAz.heqp3lzQHA1gGiQ2YBNXG9C6as21G7G
-- servicios123 -> $2b$12$4rE5Gx4XxcvMrCvxl/XYReUEbvpiy66rTF/LDzs0RRD4zUlNJ.D6G
INSERT INTO usuarios (id_usuario, nombre_usuario, id_carrera, contraseña, rol, is_active) VALUES
('admin', 'Administrador del Sistema', NULL, '$2b$12$4dGtQjmlRcIhLzEED.G.sut2y34cw7rvHCIzp/CsYPKeT2VEIQ7AK', 'admin', TRUE),
('jefe001', 'Jefe de Carrera - Sistemas', 'ING-SIS', '$2b$12$EpTN7znyFdvpf6oCBwhAz.heqp3lzQHA1gGiQ2YBNXG9C6as21G7G', 'jefe', TRUE),
('jefe002', 'Jefe de Carrera - Industrial', 'ING-IND', '$2b$12$EpTN7znyFdvpf6oCBwhAz.heqp3lzQHA1gGiQ2YBNXG9C6as21G7G', 'jefe', TRUE),
('servicios001', 'Servicios Escolares', NULL, '$2b$12$4rE5Gx4XxcvMrCvxl/XYReUEbvpiy66rTF/LDzs0RRD4zUlNJ.D6G', 'servicios', TRUE);

-- Profesores
INSERT INTO profesores (id_profesor, nombre_profesor, is_disable) VALUES
('PROF001', 'Dr. Juan Pérez García', FALSE),
('PROF002', 'Mtra. María González López', FALSE),
('PROF003', 'Dr. Carlos Rodríguez Martínez', FALSE),
('PROF004', 'Mtra. Ana Hernández Sánchez', FALSE),
('PROF005', 'Dr. Luis Fernández Torres', FALSE);

-- Periodos Académicos
INSERT INTO periodos_academicos (id_periodo, nombre_periodo) VALUES
('2024-1', 'Enero-Junio 2024'),
('2024-2', 'Agosto-Diciembre 2024'),
('2025-1', 'Enero-Junio 2025');

-- Materias
INSERT INTO materias (id_materia, nombre_materia) VALUES
('MAT001', 'Programación I'),
('MAT002', 'Base de Datos'),
('MAT003', 'Estructuras de Datos'),
('MAT004', 'Ingeniería de Software'),
('MAT005', 'Sistemas Operativos'),
('MAT006', 'Redes de Computadoras'),
('MAT007', 'Inteligencia Artificial'),
('MAT008', 'Desarrollo Web');

-- Tipos de Evaluación
INSERT INTO tipos_de_evaluacion (id_evaluacion, nombre_evaluacion) VALUES
('EVAL001', 'Ordinario'),
('EVAL002', 'Extraordinario'),
('EVAL003', 'Título de Suficiencia'),
('EVAL004', 'Regularización');

-- Aulas
INSERT INTO aulas (id_aula, nombre_aula, capacidad, is_disable) VALUES
('AULA001', 'Aula 101', 30, FALSE),
('AULA002', 'Aula 102', 35, FALSE),
('AULA003', 'Aula 201', 40, FALSE),
('AULA004', 'Aula 202', 30, FALSE),
('AULA005', 'Laboratorio de Computación 1', 25, FALSE),
('AULA006', 'Laboratorio de Computación 2', 25, FALSE),
('AULA007', 'Auditorio Principal', 100, FALSE);

-- Grupos Escolares
INSERT INTO grupos_escolares (id_grupo, nombre_grupo, numero_alumnos, id_carrera) VALUES
('GRUPO001', '1A', 30, 'ING-SIS'),
('GRUPO002', '1B', 28, 'ING-SIS'),
('GRUPO003', '2A', 32, 'ING-SIS'),
('GRUPO004', '2B', 30, 'ING-SIS'),
('GRUPO005', '3A', 25, 'ING-SIS'),
('GRUPO006', '1A', 35, 'ING-IND'),
('GRUPO007', '1B', 33, 'ING-IND'),
('GRUPO008', '2A', 30, 'ING-IND');

-- Ventanas de Aplicación por Periodo
INSERT INTO ventanas_de_aplicacion_por_periodo (id_ventana, id_periodo, id_evaluacion, fecha_inicio_examenes, fecha_fin_examenes) VALUES
('VENT001', '2024-1', 'EVAL001', '2024-06-10', '2024-06-20'),
('VENT002', '2024-1', 'EVAL002', '2024-07-01', '2024-07-15'),
('VENT003', '2024-2', 'EVAL001', '2024-12-10', '2024-12-20'),
('VENT004', '2024-2', 'EVAL002', '2025-01-05', '2025-01-20');

-- Horarios Regulares de Clase
INSERT INTO horarios_regulares_de_clase (id_horario_clase, id_periodo, id_materia, id_grupo, id_profesor, id_aula, dia_semana, hora_inicio, hora_fin) VALUES
('HOR001', '2024-1', 'MAT001', 'GRUPO001', 'PROF001', 'AULA001', 1, '08:00:00', '10:00:00'),
('HOR002', '2024-1', 'MAT001', 'GRUPO002', 'PROF001', 'AULA002', 1, '10:00:00', '12:00:00'),
('HOR003', '2024-1', 'MAT002', 'GRUPO003', 'PROF002', 'AULA005', 2, '08:00:00', '10:00:00'),
('HOR004', '2024-1', 'MAT003', 'GRUPO003', 'PROF003', 'AULA001', 3, '08:00:00', '10:00:00'),
('HOR005', '2024-1', 'MAT004', 'GRUPO005', 'PROF004', 'AULA003', 4, '10:00:00', '12:00:00'),
('HOR006', '2024-1', 'MAT005', 'GRUPO005', 'PROF005', 'AULA006', 5, '08:00:00', '10:00:00');

-- Permisos Sinodales por Materia
INSERT INTO permisos_sinodales_por_materia (id_regla, id_profesor, id_materia) VALUES
('PERM001', 'PROF001', 'MAT001'),
('PERM002', 'PROF001', 'MAT002'),
('PERM003', 'PROF002', 'MAT002'),
('PERM004', 'PROF002', 'MAT003'),
('PERM005', 'PROF003', 'MAT003'),
('PERM006', 'PROF003', 'MAT004'),
('PERM007', 'PROF004', 'MAT004'),
('PERM008', 'PROF004', 'MAT005');

-- Solicitudes de Examen
INSERT INTO solicitudes_de_examen (id_horario, id_periodo, id_evaluacion, id_materia, fecha_examen, hora_inicio, hora_fin, estado, motivo_rechazo, is_manualmente_editado) VALUES
('SOL001', '2024-1', 'EVAL001', 'MAT001', '2024-06-15', '09:00:00', '11:00:00', 1, NULL, FALSE),
('SOL002', '2024-1', 'EVAL001', 'MAT002', '2024-06-16', '09:00:00', '11:00:00', 1, NULL, FALSE),
('SOL003', '2024-1', 'EVAL002', 'MAT003', '2024-07-05', '10:00:00', '12:00:00', 0, NULL, FALSE),
('SOL004', '2024-1', 'EVAL001', 'MAT004', '2024-06-17', '08:00:00', '10:00:00', 1, NULL, FALSE);

-- Grupos por Solicitud de Examen
INSERT INTO grupos_por_solicitud_de_examen (id_examen_grupo, id_horario, id_grupo) VALUES
('EXGR001', 'SOL001', 'GRUPO001'),
('EXGR002', 'SOL001', 'GRUPO002'),
('EXGR003', 'SOL002', 'GRUPO003'),
('EXGR004', 'SOL004', 'GRUPO005');

-- Asignación Aulas y Aplicadores
INSERT INTO asignacion_aulas_y_aplicadores (id_examen_aula, id_horario, id_aula, id_profesor_aplicador) VALUES
('ASIG001', 'SOL001', 'AULA001', 'PROF001'),
('ASIG002', 'SOL001', 'AULA002', 'PROF002'),
('ASIG003', 'SOL002', 'AULA005', 'PROF002'),
('ASIG004', 'SOL004', 'AULA003', 'PROF004');

-- Asignación Sinodales
INSERT INTO asignacion_sinodales (id_examen_sinodal, id_horario, id_profesor) VALUES
('SIN001', 'SOL001', 'PROF002'),
('SIN002', 'SOL001', 'PROF003'),
('SIN003', 'SOL002', 'PROF003'),
('SIN004', 'SOL002', 'PROF004'),
('SIN005', 'SOL004', 'PROF005');

-- =====================================================
-- NOTAS IMPORTANTES
-- =====================================================
-- 1. Las contraseñas de los usuarios en este script son hashes de ejemplo
--    Para generar hashes reales, usar el script create_initial_users.py
-- 2. Los datos son de ejemplo y deben ajustarse según las necesidades reales
-- 3. En producción, cambiar todas las contraseñas por defecto
-- 4. Verificar que todas las foreign keys sean válidas antes de insertar datos

-- =====================================================
-- VERIFICAR DATOS INSERTADOS
-- =====================================================
-- SELECT COUNT(*) FROM carreras;
-- SELECT COUNT(*) FROM usuarios;
-- SELECT COUNT(*) FROM profesores;
-- SELECT COUNT(*) FROM periodos_academicos;
-- SELECT COUNT(*) FROM materias;
-- SELECT COUNT(*) FROM tipos_de_evaluacion;
-- SELECT COUNT(*) FROM aulas;
-- SELECT COUNT(*) FROM grupos_escolares;
-- SELECT COUNT(*) FROM ventanas_de_aplicacion_por_periodo;
-- SELECT COUNT(*) FROM horarios_regulares_de_clase;
-- SELECT COUNT(*) FROM permisos_sinodales_por_materia;
-- SELECT COUNT(*) FROM solicitudes_de_examen;
-- SELECT COUNT(*) FROM grupos_por_solicitud_de_examen;
-- SELECT COUNT(*) FROM asignacion_aulas_y_aplicadores;
-- SELECT COUNT(*) FROM asignacion_sinodales;
