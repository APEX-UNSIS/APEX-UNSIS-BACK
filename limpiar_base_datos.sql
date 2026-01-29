-- =====================================================
-- Script para limpiar la base de datos APEX-UNSIS
-- =====================================================
-- Mantiene solo el usuario admin. Elimina el resto de datos.
-- Scripts funcionales del proyecto: crear_tablas.sql y este.
-- =====================================================
-- Uso: psql -U tu_usuario -d tu_base_de_datos -f limpiar_base_datos.sql
-- =====================================================

SET session_replication_role = 'replica';

-- Orden inverso a las dependencias (FK)
DELETE FROM asignacion_sinodales;
DELETE FROM asignacion_aulas_y_aplicadores;
DELETE FROM grupos_por_solicitud_de_examen;
DELETE FROM solicitudes_de_examen;
DELETE FROM permisos_sinodales_por_materia;
DELETE FROM horarios_regulares_de_clase;
DELETE FROM ventanas_de_aplicacion_por_periodo;
DELETE FROM grupos_escolares;
DELETE FROM salas_de_computo;
DELETE FROM aulas;
DELETE FROM tipos_de_evaluacion;
DELETE FROM materias;
DELETE FROM periodos_academicos;
DELETE FROM profesores;
DELETE FROM carreras;
DELETE FROM usuarios WHERE id_usuario != 'admin';

SET session_replication_role = 'origin';
