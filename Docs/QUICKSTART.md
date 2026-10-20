#  Inicio Rápido - Autenticación JWT

## Pasos para configurar autenticación en tu proyecto

### 1⃣ Actualizar la Base de Datos

Ejecuta el script SQL para agregar los campos nuevos y usuarios de prueba:

```bash
psql -U tu_usuario -d apex_unsis_db -f insertar_usuarios_prueba.sql
```

O manualmente en PostgreSQL:

```sql
-- Agregar nuevos campos
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS email VARCHAR(100) UNIQUE,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;
```

### 2⃣ Configurar Variables de Entorno

Asegúrate de tener un archivo `.env` con:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=apex_unsis_db
SECRET_KEY=tu-clave-secreta-muy-segura-cambiar-en-produccion
```

### 3⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4⃣ Iniciar el Servidor

```bash
uvicorn app.main:app --reload
```

### 5⃣ Probar la Autenticación

**Opción A: Desde el navegador**
- Visita: http://localhost:8000/docs
- Prueba el endpoint `/api/v1/auth/login`

**Opción B: Con el script de prueba**
```bash
python test_auth.py
```

**Opción C: Con cURL**
```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user":"admin","password":"admin123"}'

# Guardar token y usarlo
TOKEN="tu_token_aqui"
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

##  Usuarios de Prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | admin |
| jefe1 | jefe123 | jefe |
| servicios1 | servicios123 | servicios |

##  Cómo Proteger tus Endpoints

### Método 1: Requerir autenticación básica

```python
from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user
from app.schemas.UsuarioSchema import UsuarioResponse

router = APIRouter()

@router.get("/mi-endpoint")
def mi_endpoint(current_user: UsuarioResponse = Depends(get_current_active_user)):
    return {"mensaje": f"Hola {current_user.nombre_usuario}"}
```

### Método 2: Requerir rol específico

```python
from app.dependencies import require_admin

@router.delete("/eliminar/{id}")
def eliminar_recurso(id: int, current_user = Depends(require_admin)):
    return {"mensaje": "Recurso eliminado"}
```

### Método 3: Múltiples roles permitidos

```python
from app.dependencies import require_roles

@router.post("/aprobar/{id}")
def aprobar(id: int, current_user = Depends(require_roles(["admin", "jefe"]))):
    return {"mensaje": "Aprobado"}
```

##  Integración con Frontend

### React/JavaScript Example

```javascript
// Login
const response = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ user: 'admin', password: 'admin123' })
});

const data = await response.json();
localStorage.setItem('token', data.token);

// Petición autenticada
const token = localStorage.getItem('token');
const response = await fetch('http://localhost:8000/api/v1/auth/me', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

##  Documentación Completa

Lee el archivo `AUTH_GUIDE.md` para documentación detallada.

##  Importante

- En producción, genera una `SECRET_KEY` segura: `openssl rand -hex 32`
- Usa HTTPS siempre en producción
- Cambia las contraseñas de prueba

##  Problemas Comunes

**Error 401 "No se pudieron validar las credenciales"**
- Verifica que envías el header: `Authorization: Bearer <token>`
- El token puede haber expirado

**Error 401 "Usuario o contraseña incorrectos"**
- Verifica que el usuario existe en la BD
- Asegúrate de usar las contraseñas correctas

**Error 403 "No tienes permisos suficientes"**
- Tu usuario no tiene el rol requerido para ese endpoint
