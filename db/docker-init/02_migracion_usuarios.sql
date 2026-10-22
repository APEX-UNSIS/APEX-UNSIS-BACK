-- =====================================================
-- Migración: columnas de `usuarios` que exige el modelo SQLAlchemy
-- =====================================================
-- El modelo app/features/usuarios/domain/models.py define email, created_at
-- y last_login, pero crear_tablas.sql no las creaba. Sin estas columnas el
-- ORM falla al hacer login con:
--   sqlalchemy.exc.ProgrammingError: column "usuarios.email" does not exist
--
-- Es idempotente: se puede aplicar sobre una base ya creada.
-- =====================================================

ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS email VARCHAR(100) UNIQUE;
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE usuarios ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;

-- Backfill por si la tabla ya tenía filas
UPDATE usuarios SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL;
