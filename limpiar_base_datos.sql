-- =====================================================
-- Script para limpiar la base de datos APEX-UNSIS
-- Mantiene solo el usuario admin
-- =====================================================
-- ADVERTENCIA: Este script elimina TODOS los datos excepto el usuario admin
-- Ejecutar con precaución
-- =====================================================
-- Uso: psql -U tu_usuario -d tu_base_de_datos -f limpiar_base_datos.sql
-- =====================================================

-- Desactivar temporalmente las restricciones de foreign key
SET session_replication_role = 'replica';

-- Eliminar datos de tablas dependientes (en orden inverso de dependencias)
DELETE FROM asignacion_sinodales;
DELETE FROM asignacion_aulas_y_aplicadores;
DELETE FROM grupos_por_solicitud_de_examen;
DELETE FROM solicitudes_de_examen;
DELETE FROM permisos_sinodales_por_materia;
DELETE FROM horarios_regulares_de_clase;
DELETE FROM ventanas_de_aplicacion_por_periodo;
DELETE FROM grupos_escolares;
DELETE FROM aulas;
DELETE FROM tipos_de_evaluacion;
DELETE FROM materias;
DELETE FROM periodos_academicos;
DELETE FROM profesores;
DELETE FROM carreras;

-- Eliminar usuarios excepto admin
DELETE FROM usuarios WHERE id_usuario != 'admin';

-- Reactivar restricciones de foreign key
SET session_replication_role = 'origin';

-- =====================================================
-- Verificar que solo queda el usuario admin
-- =====================================================
-- SELECT * FROM usuarios;
-- SELECT COUNT(*) as total_usuarios FROM usuarios;
-- =====================================================
