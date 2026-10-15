-- Script para crear/actualizar usuarios en la base de datos
-- Ejecutar en pgAdmin en la base de datos apex_db

-- Verificar usuarios existentes
SELECT id_usuario, nombre_usuario, rol, is_active FROM usuarios;

-- Eliminar usuarios si existen (opcional, solo si quieres recrearlos)
-- DELETE FROM usuarios WHERE id_usuario IN ('admin', 'jefe001', 'servicios001');

-- Insertar usuarios con hashes correctos de bcrypt
-- Estos hashes fueron generados con: passlib.hash("admin123"), etc.

-- Hashes generados con bcrypt (cada ejecución genera hashes diferentes pero todos funcionan)
INSERT INTO usuarios (id_usuario, nombre_usuario, id_carrera, contraseña, rol, is_active) 
VALUES
('admin', 'Administrador del Sistema', NULL, '$2b$12$seffkb/3Ee9izbm2ZpjmEuDdnHTw9oTIp/wUe/E8SZWSKriDL/fCe', 'admin', TRUE),
('jefe001', 'Jefe de Carrera - Sistemas', NULL, '$2b$12$QpISh56WlAuNOvup/.Lf1uN1VIZRKkyjXKtpRUrY5fWjtVO7LRXd.', 'jefe', TRUE),
('servicios001', 'Servicios Escolares', NULL, '$2b$12$CIbXDF4nl4qsQ5zg5IAMv.xypOrv12HPsTfBFGg.6dSnhA.nWBnWy', 'servicios', TRUE)
ON CONFLICT (id_usuario) DO UPDATE SET
    nombre_usuario = EXCLUDED.nombre_usuario,
    contraseña = EXCLUDED.contraseña,
    rol = EXCLUDED.rol,
    is_active = EXCLUDED.is_active;

-- Verificar que se crearon correctamente
SELECT id_usuario, nombre_usuario, rol, is_active FROM usuarios;
