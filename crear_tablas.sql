-- =====================================================
-- Script para crear las tablas de la base de datos APEX-UNSIS
-- =====================================================
-- Última versión: incluye materias.es_academia, materias.tipo_examen, tabla salas_de_computo
-- (tipos de examen: 'escrito' | 'plataforma'; por defecto: plataforma)
-- salas_de_computo: lista de id_aula que son salas de cómputo (exámenes en plataforma); no son materias.
-- Este script crea las tablas, usuario admin y asegura columnas de materias.
-- Ejecutar en pgAdmin o psql después de crear la base de datos.
-- =====================================================

-- =====================================================
-- CREAR TABLAS
-- =====================================================

-- Tabla: carreras
CREATE TABLE IF NOT EXISTS carreras (
    id_carrera VARCHAR(20) PRIMARY KEY,
    nombre_carrera VARCHAR(100)
);

-- Tabla: usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario VARCHAR(50) PRIMARY KEY,
    nombre_usuario VARCHAR(100) NOT NULL,
    id_carrera VARCHAR(20),
    contraseña VARCHAR(255) NOT NULL,
    rol VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_usuario_carrera FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);

-- Tabla: profesores
CREATE TABLE IF NOT EXISTS profesores (
    id_profesor VARCHAR(20) PRIMARY KEY,
    nombre_profesor VARCHAR(60),
    is_disable BOOLEAN DEFAULT FALSE
);

-- Tabla: periodos_academicos
CREATE TABLE IF NOT EXISTS periodos_academicos (
    id_periodo VARCHAR(20) PRIMARY KEY,
    nombre_periodo VARCHAR(30)
);

-- Tabla: materias (incluye es_academia y tipo_examen: 'escrito' | 'plataforma')
CREATE TABLE IF NOT EXISTS materias (
    id_materia VARCHAR(20) PRIMARY KEY,
    nombre_materia VARCHAR(50),
    es_academia BOOLEAN DEFAULT FALSE,
    tipo_examen VARCHAR(20) DEFAULT 'plataforma'
);

-- Tabla: tipos_de_evaluacion
CREATE TABLE IF NOT EXISTS tipos_de_evaluacion (
    id_evaluacion VARCHAR(20) PRIMARY KEY,
    nombre_evaluacion VARCHAR(30)
);

-- Tabla: aulas
CREATE TABLE IF NOT EXISTS aulas (
    id_aula VARCHAR(20) PRIMARY KEY,
    nombre_aula VARCHAR(50),
    capacidad INTEGER,
    is_disable BOOLEAN DEFAULT FALSE
);

-- Tabla: salas_de_computo (aulas que son sala de cómputo para exámenes en plataforma; no son materias)
CREATE TABLE IF NOT EXISTS salas_de_computo (
    id_aula VARCHAR(20) PRIMARY KEY,
    CONSTRAINT fk_sala_computo_aula FOREIGN KEY (id_aula) REFERENCES aulas(id_aula)
);

-- Tabla: grupos_escolares
CREATE TABLE IF NOT EXISTS grupos_escolares (
    id_grupo VARCHAR(20) PRIMARY KEY,
    nombre_grupo VARCHAR(20),
    numero_alumnos INTEGER,
    id_carrera VARCHAR(20),
    CONSTRAINT fk_grupo_carrera FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);

-- Tabla: ventanas_de_aplicacion_por_periodo
CREATE TABLE IF NOT EXISTS ventanas_de_aplicacion_por_periodo (
    id_ventana VARCHAR(20) PRIMARY KEY,
    id_periodo VARCHAR(20),
    id_evaluacion VARCHAR(20),
    fecha_inicio_examenes DATE,
    fecha_fin_examenes DATE,
    CONSTRAINT fk_ventana_periodo FOREIGN KEY (id_periodo) REFERENCES periodos_academicos(id_periodo),
    CONSTRAINT fk_ventana_evaluacion FOREIGN KEY (id_evaluacion) REFERENCES tipos_de_evaluacion(id_evaluacion)
);

-- Tabla: horarios_regulares_de_clase
CREATE TABLE IF NOT EXISTS horarios_regulares_de_clase (
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
CREATE TABLE IF NOT EXISTS permisos_sinodales_por_materia (
    id_regla VARCHAR(20) PRIMARY KEY,
    id_profesor VARCHAR(20),
    id_materia VARCHAR(20),
    CONSTRAINT fk_permiso_profesor FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor),
    CONSTRAINT fk_permiso_materia FOREIGN KEY (id_materia) REFERENCES materias(id_materia)
);

-- Tabla: solicitudes_de_examen
CREATE TABLE IF NOT EXISTS solicitudes_de_examen (
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
CREATE TABLE IF NOT EXISTS grupos_por_solicitud_de_examen (
    id_examen_grupo VARCHAR(20) PRIMARY KEY,
    id_horario VARCHAR(20),
    id_grupo VARCHAR(20),
    CONSTRAINT fk_examen_grupo_solicitud FOREIGN KEY (id_horario) REFERENCES solicitudes_de_examen(id_horario),
    CONSTRAINT fk_examen_grupo_grupo FOREIGN KEY (id_grupo) REFERENCES grupos_escolares(id_grupo)
);

-- Tabla: asignacion_aulas_y_aplicadores
CREATE TABLE IF NOT EXISTS asignacion_aulas_y_aplicadores (
    id_examen_aula VARCHAR(20) PRIMARY KEY,
    id_horario VARCHAR(20),
    id_aula VARCHAR(20),
    id_profesor_aplicador VARCHAR(20),
    CONSTRAINT fk_asignacion_aula_solicitud FOREIGN KEY (id_horario) REFERENCES solicitudes_de_examen(id_horario),
    CONSTRAINT fk_asignacion_aula_aula FOREIGN KEY (id_aula) REFERENCES aulas(id_aula),
    CONSTRAINT fk_asignacion_aula_profesor FOREIGN KEY (id_profesor_aplicador) REFERENCES profesores(id_profesor)
);

-- Tabla: asignacion_sinodales
CREATE TABLE IF NOT EXISTS asignacion_sinodales (
    id_examen_sinodal VARCHAR(20) PRIMARY KEY,
    id_horario VARCHAR(20),
    id_profesor VARCHAR(20),
    CONSTRAINT fk_asignacion_sinodal_solicitud FOREIGN KEY (id_horario) REFERENCES solicitudes_de_examen(id_horario),
    CONSTRAINT fk_asignacion_sinodal_profesor FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor)
);

-- =====================================================
-- DATOS INICIALES: TIPOS DE EVALUACIÓN
-- =====================================================
INSERT INTO tipos_de_evaluacion (id_evaluacion, nombre_evaluacion) VALUES
('EVAL001', 'Parcial 1'),
('EVAL002', 'Parcial 2'),
('EVAL003', 'Parcial 3'),
('EVAL004', 'Ordinario')
ON CONFLICT (id_evaluacion) DO NOTHING;

-- =====================================================
-- CREAR USUARIO ADMIN POR DEFECTO
-- =====================================================
-- Contraseña: admin123 -> $2b$12$4dGtQjmlRcIhLzEED.G.sut2y34cw7rvHCIzp/CsYPKeT2VEIQ7AK
INSERT INTO usuarios (id_usuario, nombre_usuario, id_carrera, contraseña, rol, is_active) 
VALUES ('admin', 'Administrador del Sistema', NULL, '$2b$12$4dGtQjmlRcIhLzEED.G.sut2y34cw7rvHCIzp/CsYPKeT2VEIQ7AK', 'admin', TRUE)
ON CONFLICT (id_usuario) DO NOTHING;

-- =====================================================
-- MIGRACIÓN: COLUMNAS DE MATERIAS (es_academia, tipo_examen)
-- =====================================================
-- Si la tabla materias ya existía sin estas columnas, agregarlas.
-- Tipos de examen válidos: 'escrito' | 'plataforma' (por defecto: plataforma)
ALTER TABLE materias ADD COLUMN IF NOT EXISTS es_academia BOOLEAN DEFAULT FALSE;
ALTER TABLE materias ADD COLUMN IF NOT EXISTS tipo_examen VARCHAR(20) DEFAULT 'plataforma';
-- Asegurar que todas las materias tengan valores definidos (no se agregan automáticamente al sincronizar)
UPDATE materias SET tipo_examen = 'plataforma' WHERE tipo_examen IS NULL;
UPDATE materias SET es_academia = FALSE WHERE es_academia IS NULL;

-- =====================================================
-- SALAS DE CÓMPUTO (opcional)
-- =====================================================
-- Insertar aquí los id_aula que son salas de cómputo (para exámenes en plataforma).
-- Ejemplo (ajustar ids según tus aulas): INSERT INTO salas_de_computo (id_aula) VALUES ('71'), ('72') ON CONFLICT (id_aula) DO NOTHING;

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================
