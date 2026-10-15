#  Comandos Rápidos - Autenticación JWT

##  Setup Inicial (Una sola vez)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Crear base de datos (si no existe)
psql -U postgres
CREATE DATABASE apex_db;
\q

# 3. Configurar usuarios de prueba
psql -U tu_usuario -d apex_db -f insertar_usuarios_prueba.sql

# 4. Verificar .env tiene SECRET_KEY
cat .env | grep SECRET_KEY
```

---

##  Iniciar Servidor

```bash
# Modo desarrollo (con recarga automática)
uvicorn app.main:app --reload

# O en modo producción
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

##  Probar Autenticación

### Opción 1: Script Python
```bash
python test_auth.py
```

### Opción 2: Frontend HTML
```bash
# Abre en el navegador
firefox ejemplo_frontend_login.html
# o
chromium ejemplo_frontend_login.html
```

### Opción 3: cURL

**Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user":"admin","password":"admin123"}'
```

**Guardar token en variable:**
```bash
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user":"admin","password":"admin123"}' | jq -r '.token')

echo $TOKEN
```

**Obtener usuario actual:**
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

**Endpoint protegido:**
```bash
curl -X GET "http://localhost:8000/api/v1/ejemplo/protegido" \
  -H "Authorization: Bearer $TOKEN"
```

### Opción 4: httpie (si lo tienes instalado)

```bash
# Login
http POST localhost:8000/api/v1/auth/login user=admin password=admin123

# Con token
http GET localhost:8000/api/v1/auth/me "Authorization:Bearer TOKEN_AQUI"
```

---

##  Generar Hashes de Contraseña

```bash
# Genera hashes para usuarios de prueba
python generar_hashes.py

# O en Python interactivo
python3 << EOF
import bcrypt
password = "mi_password"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
print(hashed.decode('utf-8'))
EOF
```

---

##  Comandos PostgreSQL

### Verificar usuarios
```bash
psql -U tu_usuario -d apex_db -c "SELECT id_usuario, nombre_usuario, rol, is_active FROM usuarios;"
```

### Ver estructura de tabla
```bash
psql -U tu_usuario -d apex_db -c "\d usuarios"
```

### Agregar campos nuevos manualmente
```bash
psql -U tu_usuario -d apex_db << EOF
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS email VARCHAR(100) UNIQUE,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;
EOF
```

### Insertar usuario manualmente
```bash
psql -U tu_usuario -d apex_db << 'EOF'
INSERT INTO usuarios (id_usuario, nombre_usuario, contraseña, rol, is_active)
VALUES (
  'test_user',
  'Usuario de Prueba',
  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYILSq7K0oG',
  'servicios',
  true
);
EOF
```

### Actualizar contraseña de un usuario
```bash
# 1. Genera el hash primero
python3 -c "import bcrypt; print(bcrypt.hashpw('nueva_password'.encode(), bcrypt.gensalt()).decode())"

# 2. Actualiza en BD (reemplaza el hash)
psql -U tu_usuario -d apex_db << 'EOF'
UPDATE usuarios 
SET contraseña = '$2b$12$NUEVO_HASH_AQUI'
WHERE id_usuario = 'admin';
EOF
```

---

##  Debugging

### Ver logs del servidor
```bash
# Si usas uvicorn con --reload, los logs se muestran en consola
# Para debug más detallado:
uvicorn app.main:app --reload --log-level debug
```

### Verificar token JWT
```bash
# Decodificar token (sin verificar firma)
python3 << EOF
import jwt
token = "TU_TOKEN_AQUI"
decoded = jwt.decode(token, options={"verify_signature": False})
print(decoded)
EOF
```

### Verificar conexión a BD
```bash
python3 << EOF
from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(" Conexión exitosa")
EOF
```

---

##  Testing

### Probar todos los endpoints
```bash
python test_auth.py
```

### Probar solo login
```bash
python3 << EOF
import requests
response = requests.post(
    'http://localhost:8000/api/v1/auth/login',
    json={'user': 'admin', 'password': 'admin123'}
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
EOF
```

---

##  Mantenimiento

### Listar usuarios activos
```bash
psql -U tu_usuario -d apex_db -c \
  "SELECT id_usuario, nombre_usuario, rol, last_login FROM usuarios WHERE is_active = true;"
```

### Desactivar usuario
```bash
psql -U tu_usuario -d apex_db -c \
  "UPDATE usuarios SET is_active = false WHERE id_usuario = 'usuario_a_desactivar';"
```

### Resetear contraseña
```bash
# 1. Generar nuevo hash
NEW_HASH=$(python3 -c "import bcrypt; print(bcrypt.hashpw('nueva_password'.encode(), bcrypt.gensalt()).decode())")

# 2. Actualizar en BD
psql -U tu_usuario -d apex_db -c \
  "UPDATE usuarios SET contraseña = '$NEW_HASH' WHERE id_usuario = 'admin';"
```

---

##  Swagger UI

### Acceder a la documentación interactiva
```bash
# Abre en navegador
firefox http://localhost:8000/docs

# O prueba directamente desde terminal
curl http://localhost:8000/docs
```

### Probar login desde Swagger
1. Abre http://localhost:8000/docs
2. Busca `POST /api/v1/auth/login`
3. Click en "Try it out"
4. Ingresa: `{"user":"admin","password":"admin123"}`
5. Click "Execute"
6. Copia el token de la respuesta
7. Click en "Authorize" (arriba a la derecha)
8. Pega el token y click "Authorize"
9. Ahora puedes probar endpoints protegidos

---

##  Git

### Verificar que .env no esté en git
```bash
git status | grep .env
# No debería aparecer .env (solo .env.example)

# Si aparece, agregarlo a .gitignore
echo ".env" >> .gitignore
git rm --cached .env
git commit -m "Remove .env from git"
```

---

##  Seguridad en Producción

### Generar SECRET_KEY segura
```bash
# Opción 1: openssl
openssl rand -hex 32

# Opción 2: Python
python3 -c "import secrets; print(secrets.token_hex(32))"

# Actualizar en .env
echo "SECRET_KEY=$(openssl rand -hex 32)" >> .env
```

### Verificar SECRET_KEY actual
```bash
grep SECRET_KEY .env
```

---

##  Comandos Útiles para Desarrollo

### Ver todas las rutas disponibles
```bash
python3 << EOF
from app.main import app
for route in app.routes:
    if hasattr(route, 'methods'):
        print(f"{list(route.methods)[0]:6} {route.path}")
EOF
```

### Verificar dependencias instaladas
```bash
pip list | grep -E "fastapi|uvicorn|bcrypt|jose|passlib"
```

### Reinstalar dependencias
```bash
pip install -r requirements.txt --upgrade
```

---

##  Limpieza

### Eliminar todos los usuarios de prueba
```bash
psql -U tu_usuario -d apex_db -c \
  "DELETE FROM usuarios WHERE id_usuario IN ('admin', 'jefe1', 'jefe2', 'servicios1');"
```

### Resetear tabla usuarios
```bash
psql -U tu_usuario -d apex_db << 'EOF'
TRUNCATE TABLE usuarios CASCADE;
EOF
```

---

##  Variables de Entorno Rápidas

### Ver todas las variables
```bash
cat .env
```

### Establecer variables temporalmente
```bash
export DB_USER=mi_usuario
export DB_PASSWORD=mi_password
uvicorn app.main:app --reload
```

---

##  One-Liners Útiles

```bash
# Login rápido y guardar token
export TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user":"admin","password":"admin123"}' | jq -r '.token')

# Hacer petición autenticada
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/auth/me

# Contar usuarios activos
psql -U tu_usuario -d apex_db -tAc "SELECT COUNT(*) FROM usuarios WHERE is_active = true;"

# Ver último login de todos los usuarios
psql -U tu_usuario -d apex_db -c \
  "SELECT id_usuario, last_login FROM usuarios ORDER BY last_login DESC;"

# Generar y mostrar hash de una contraseña
python3 -c "import bcrypt; import sys; print(bcrypt.hashpw(sys.argv[1].encode(), bcrypt.gensalt()).decode())" "mi_password"
```

---

##  Troubleshooting Rápido

```bash
# Si el servidor no inicia - verificar puerto
lsof -i :8000

# Si falla la conexión a BD - verificar PostgreSQL
systemctl status postgresql
# o
sudo service postgresql status

# Si falta alguna dependencia
pip install -r requirements.txt --force-reinstall

# Si hay error con bcrypt
pip uninstall bcrypt
pip install bcrypt

# Limpiar caché de Python
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

---

** Tip:** Guarda este archivo y úsalo como referencia rápida!
