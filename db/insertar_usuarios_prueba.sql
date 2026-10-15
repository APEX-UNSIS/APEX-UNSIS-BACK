-- Script para actualizar la tabla usuarios con los campos nuevos
-- Ejecutar este script después de agregar los campos en el modelo Usuario

-- Agregar campos adicionales a la tabla usuarios si no existen
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS email VARCHAR(100) UNIQUE,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;

-- Insertar usuarios de prueba
-- NOTA: Los hashes de contraseña deben generarse con el script generar_hashes.py
-- Estos son ejemplos con contraseñas hasheadas (password: admin123, jefe123, servicios123)

-- Usuario Administrador (user: admin, password: admin123)
INSERT INTO usuarios (id_usuario, nombre_usuario, email, contraseña, rol, is_active, created_at)
VALUES (
    'admin',
    'Administrador Sistema',
    'admin@apex.unsis.edu',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILSq7K0oG',
    'admin',
    true,
    CURRENT_TIMESTAMP
) ON CONFLICT (id_usuario) DO UPDATE SET
    contraseña = EXCLUDED.contraseña,
    email = EXCLUDED.email;

-- Usuario Jefe de Carrera (user: jefe1, password: jefe123)
INSERT INTO usuarios (id_usuario, nombre_usuario, email, contraseña, rol, is_active, id_carrera, created_at)
VALUES (
    'jefe1',
    'Jefe Carrera Informática',
    'jefe.informatica@apex.unsis.edu',
    '$2b$12$EixZX0fB5x5qH0YK5TqPUeVhI1YJYF.zKvhE9yP0.vY7dGPKqH5Ri',
    'jefe',
    true,
    'A06LI06',
    CURRENT_TIMESTAMP
) ON CONFLICT (id_usuario) DO UPDATE SET
    contraseña = EXCLUDED.contraseña,
    email = EXCLUDED.email;

-- Usuario de Servicios Escolares (user: servicios1, password: servicios123)
INSERT INTO usuarios (id_usuario, nombre_usuario, email, contraseña, rol, is_active, created_at)
VALUES (
    'servicios1',
    'Personal Servicios Escolares',
    'servicios@apex.unsis.edu',
    '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi',
    'servicios',
    true,
    CURRENT_TIMESTAMP
) ON CONFLICT (id_usuario) DO UPDATE SET
    contraseña = EXCLUDED.contraseña,
    email = EXCLUDED.email;

-- Usuario Jefe de Industrial (user: jefe2, password: jefe123)
INSERT INTO usuarios (id_usuario, nombre_usuario, email, contraseña, rol, is_active, id_carrera, created_at)
VALUES (
    'jefe2',
    'Jefe Carrera Medicina',
    'jefe.medicina@apex.unsis.edu',
    '$2b$12$EixZX0fB5x5qH0YK5TqPUeVhI1YJYF.zKvhE9yP0.vY7dGPKqH5Ri',
    'jefe',
    true,
    'A06LM07',
    CURRENT_TIMESTAMP
) ON CONFLICT (id_usuario) DO UPDATE SET
    contraseña = EXCLUDED.contraseña,
    email = EXCLUDED.email;

-- Verificar los usuarios creados
SELECT id_usuario, nombre_usuario, email, rol, is_active, created_at 
FROM usuarios 
ORDER BY created_at DESC;
