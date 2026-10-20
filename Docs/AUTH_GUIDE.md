# Guía de Autenticación JWT - APEX UNSIS Backend

##  Descripción

Este backend implementa autenticación JWT (JSON Web Tokens) para proteger los endpoints de la API. Los usuarios deben autenticarse para obtener un token que les permita acceder a los recursos protegidos.

##  Roles de Usuario

El sistema soporta tres tipos de roles:

- **admin**: Administrador del sistema (acceso completo)
- **jefe**: Jefe de carrera (acceso a recursos de su carrera)
- **servicios**: Personal de servicios escolares (acceso a gestión de solicitudes)

##  Configuración Inicial

### 1. Variables de Entorno

Crea un archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Edita el archivo `.env` y configura:

```env
# Base de datos
DB_HOST=localhost
DB_PORT=5432
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=apex_unsis_db

# JWT Secret Key (¡IMPORTANTE! Cambia esto en producción)
SECRET_KEY=tu-clave-secreta-muy-segura-cambiar-en-produccion-minimo-32-caracteres
```

**Generar una SECRET_KEY segura:**
```bash
openssl rand -hex 32
```

### 2. Crear Usuarios de Prueba

Ejecuta el script SQL para crear usuarios de prueba:

```bash
psql -U tu_usuario -d apex_unsis_db -f insertar_usuarios_prueba.sql
```

**Usuarios de prueba creados:**

| Usuario | Contraseña | Rol | Email |
|---------|------------|-----|-------|
| admin | admin123 | admin | admin@apex.unsis.edu |
| jefe1 | jefe123 | jefe | jefe.sistemas@apex.unsis.edu |
| jefe2 | jefe123 | jefe | jefe.industrial@apex.unsis.edu |
| servicios1 | servicios123 | servicios | servicios@apex.unsis.edu |

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el Servidor

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en: `http://localhost:8000`

##  Endpoints de Autenticación

### 1. Login (Obtener Token)

**POST** `/api/v1/auth/login`

Autentica un usuario y retorna un token JWT.

**Request Body:**
```json
{
  "user": "admin",
  "password": "admin123"
}
```

**Response:** (200 OK)
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id_usuario": "admin",
    "nombre_usuario": "Administrador Sistema",
    "email": "admin@apex.unsis.edu",
    "rol": "admin",
    "is_active": true,
    "created_at": "2026-01-20T10:00:00",
    "last_login": null
  }
}
```

**Errores:**
- `401 Unauthorized`: Credenciales incorrectas
- `500 Internal Server Error`: Error del servidor

### 2. Obtener Usuario Actual

**GET** `/api/v1/auth/me`

Obtiene la información del usuario autenticado.

**Headers:**
```
Authorization: Bearer <tu_token_jwt>
```

**Response:** (200 OK)
```json
{
  "id_usuario": "admin",
  "nombre_usuario": "Administrador Sistema",
  "email": "admin@apex.unsis.edu",
  "rol": "admin",
  "is_active": true,
  "created_at": "2026-01-20T10:00:00",
  "last_login": "2026-01-20T11:30:00"
}
```

##  Proteger Endpoints

### Opción 1: Requerir Usuario Autenticado

```python
from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user
from app.schemas.UsuarioSchema import UsuarioResponse

router = APIRouter()

@router.get("/mi-recurso")
def obtener_recurso(current_user: UsuarioResponse = Depends(get_current_active_user)):
    return {
        "mensaje": f"Hola {current_user.nombre_usuario}",
        "data": "datos protegidos"
    }
```

### Opción 2: Requerir Rol Específico

```python
from fastapi import APIRouter, Depends
from app.dependencies import require_admin, require_roles
from app.schemas.UsuarioSchema import UsuarioResponse

router = APIRouter()

# Solo administradores
@router.delete("/usuarios/{id}")
def eliminar_usuario(
    id: str,
    current_user: UsuarioResponse = Depends(require_admin)
):
    return {"mensaje": "Usuario eliminado"}

# Administradores o Jefes
@router.post("/solicitudes/aprobar/{id}")
def aprobar_solicitud(
    id: str,
    current_user: UsuarioResponse = Depends(require_roles(["admin", "jefe"]))
):
    return {"mensaje": "Solicitud aprobada"}
```

### Opción 3: A Nivel de Router

```python
from fastapi import APIRouter, Depends
from app.dependencies import require_admin

# Todas las rutas de este router requieren ser admin
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)]
)

@router.get("/estadisticas")
def obtener_estadisticas():
    return {"total_usuarios": 100}
```

##  Ejemplos de Uso con Fetch (Frontend)

### Login

```javascript
async function login(username, password) {
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user: username,
        password: password
      })
    });

    if (!response.ok) {
      throw new Error('Credenciales incorrectas');
    }

    const data = await response.json();
    
    // Guardar token en localStorage
    localStorage.setItem('token', data.token);
    localStorage.setItem('user', JSON.stringify(data.user));
    
    return data;
  } catch (error) {
    console.error('Error en login:', error);
    throw error;
  }
}
```

### Hacer Peticiones Autenticadas

```javascript
async function obtenerDatosProtegidos() {
  const token = localStorage.getItem('token');
  
  if (!token) {
    throw new Error('No hay sesión activa');
  }

  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/me', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    });

    if (response.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      throw new Error('Sesión expirada');
    }

    if (!response.ok) {
      throw new Error('Error al obtener datos');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}
```

### Logout

```javascript
function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  window.location.href = '/login';
}
```

##  Pruebas con cURL

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"user":"admin","password":"admin123"}'
```

### Obtener Usuario Actual
```bash
TOKEN="tu_token_aqui"

curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

##  Pruebas con Postman

1. **Configurar Variable de Entorno:**
   - En Postman, crea una variable `token` en el environment

2. **Login:**
   - POST `http://localhost:8000/api/v1/auth/login`
   - Body (JSON):
     ```json
     {
       "user": "admin",
       "password": "admin123"
     }
     ```
   - En Tests, agrega:
     ```javascript
     pm.environment.set("token", pm.response.json().token);
     ```

3. **Peticiones Autenticadas:**
   - En Headers agrega:
     ```
     Authorization: Bearer {{token}}
     ```

##  Troubleshooting

### Error: "No se pudieron validar las credenciales"
- Verifica que el token esté en el header `Authorization: Bearer <token>`
- El token puede haber expirado (duración: 30 días por defecto)

### Error: "Usuario o contraseña incorrectos"
- Verifica que el usuario exista en la base de datos
- Asegúrate de que la contraseña esté hasheada con bcrypt

### Error: "No tienes permisos suficientes"
- El usuario no tiene el rol requerido para acceder al endpoint

##  Notas de Seguridad

1. **Nunca compartas tu SECRET_KEY**: Usa una diferente en producción
2. **HTTPS en producción**: Siempre usa HTTPS para proteger los tokens
3. **Rotación de tokens**: Implementa refresh tokens para mayor seguridad
4. **Contraseñas fuertes**: En producción usa políticas de contraseñas robustas
5. **Rate Limiting**: Implementa límite de intentos de login

##  Recursos Adicionales

- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [JWT.io](https://jwt.io/) - Decodificador de tokens JWT
- [bcrypt](https://github.com/pyca/bcrypt/) - Librería de hashing

##  Soporte

Para dudas o problemas, contacta al equipo de desarrollo.
