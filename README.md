# API REST - APEX UNSIS Backend

> API REST con FastAPI y PostgreSQL - Sistema de gestión de exámenes profesionales con autenticación JWT

**URL Base:** `http://localhost:8000`

**Documentación Completa:** Ver carpeta `/docs` para guías de configuración e implementación

---

## Autenticación JWT

La API utiliza tokens JWT (JSON Web Tokens) para autenticación. Todos los endpoints protegidos requieren un token válido en el header `Authorization`.

### Roles disponibles:
- **admin**: Acceso total al sistema
- **jefe**: Gestión de su carrera (solicitudes, sinodales, grupos)
- **servicios**: Gestión operativa (aulas, horarios, calendarios)

---

## Endpoints de Autenticación

### 1. Login

Autentica un usuario y obtiene un token JWT.

**Endpoint:** `POST /api/v1/auth/login`

**Request Body:**
```json
{
  "user": "admin",
  "password": "admin123"
}
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id_usuario": "admin",
    "nombre_usuario": "Administrador Sistema",
    "email": "admin@apex.unsis.edu",
    "id_carrera": null,
    "rol": "admin",
    "is_active": true,
    "created_at": "2026-01-20T10:00:00",
    "last_login": "2026-01-20T11:30:00"
  }
}
```

**Errores:**
- `401 Unauthorized`: Credenciales incorrectas
- `500 Internal Server Error`: Error del servidor

### 2. Obtener Usuario Actual

Obtiene información del usuario autenticado.

**Endpoint:** `GET /api/v1/auth/me`

**Headers:**
```
Authorization: Bearer <tu_token_jwt>
```

**Response (200 OK):**
```json
{
  "id_usuario": "admin",
  "nombre_usuario": "Administrador Sistema",
  "email": "admin@apex.unsis.edu",
  "id_carrera": null,
  "rol": "admin",
  "is_active": true,
  "created_at": "2026-01-20T10:00:00",
  "last_login": "2026-01-20T11:30:00"
}
```

**Errores:**
- `401 Unauthorized`: Token inválido o expirado
- `403 Forbidden`: Usuario inactivo

---

## Integración con Frontend

### JavaScript / React / Vue

#### 2. Hacer Peticiones Autenticadas

```javascript
async function fetchProtectedData() {
  const token = localStorage.getItem('token');
  
  const response = await fetch('http://localhost:8000/api/v1/solicitudes', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    }
  });

  if (response.status === 401) {
    // Token expirado - redirigir a login
    localStorage.removeItem('token');
    window.location.href = '/login';
    return;
  }

  return await response.json();
}
```

#### 3. Interceptor para Axios

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

// Agregar token automáticamente
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

#### 4. Logout

```javascript
function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  window.location.href = '/login';
}
```

---

## Usuarios de Prueba

Para desarrollo y pruebas:

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| `admin` | `admin123` | admin | Acceso total |
| `jefe1` | `jefe123` | jefe | Gestión de carrera SIS |
| `jefe2` | `jefe123` | jefe | Gestión de carrera IND |
| `servicios1` | `servicios123` | servicios | Operaciones administrativas |

---

## Endpoints Principales

### Carreras
- `GET /api/v1/carreras` - Listar carreras
- `GET /api/v1/carreras/{id}` - Obtener carrera
- `POST /api/v1/carreras` - Crear carrera (admin)
- `PUT /api/v1/carreras/{id}` - Actualizar carrera (admin)

### Solicitudes de Examen
- `GET /api/v1/solicitudes` - Listar solicitudes
- `GET /api/v1/solicitudes/{id}` - Obtener solicitud
- `POST /api/v1/solicitudes` - Crear solicitud
- `PUT /api/v1/solicitudes/{id}` - Actualizar solicitud
- `DELETE /api/v1/solicitudes/{id}` - Eliminar solicitud

### Profesores
- `GET /api/v1/profesores` - Listar profesores
- `GET /api/v1/profesores/{id}` - Obtener profesor
- `POST /api/v1/profesores` - Crear profesor
- `PUT /api/v1/profesores/{id}` - Actualizar profesor

### Aulas
- `GET /api/v1/aulas` - Listar aulas
- `GET /api/v1/aulas/{id}` - Obtener aula
- `POST /api/v1/aulas` - Crear aula (admin)
- `PUT /api/v1/aulas/{id}` - Actualizar aula (admin)

### Grupos
- `GET /api/v1/grupos` - Listar grupos
- `GET /api/v1/grupos/{id}` - Obtener grupo
- `POST /api/v1/grupos` - Crear grupo
- `PUT /api/v1/grupos/{id}` - Actualizar grupo

### Materias
- `GET /api/v1/materias` - Listar materias
- `GET /api/v1/materias/{id}` - Obtener materia
- `POST /api/v1/materias` - Crear materia (admin)

### Periodos Académicos
- `GET /api/v1/periodos` - Listar periodos
- `GET /api/v1/periodos/{id}` - Obtener periodo
- `POST /api/v1/periodos` - Crear periodo (admin)

### Tipos de Evaluación
- `GET /api/v1/evaluaciones` - Listar tipos de evaluación
- `GET /api/v1/evaluaciones/{id}` - Obtener tipo
- `POST /api/v1/evaluaciones` - Crear tipo (admin)

### Horarios
- `GET /api/v1/horarios` - Listar horarios de clases
- `GET /api/v1/horarios/{id}` - Obtener horario
- `POST /api/v1/horarios` - Crear horario

### Ventanas de Aplicación
- `GET /api/v1/ventanas` - Listar ventanas
- `GET /api/v1/ventanas/{id}` - Obtener ventana
- `POST /api/v1/ventanas` - Crear ventana (admin)

### Permisos de Sinodales
- `GET /api/v1/permisos` - Listar permisos
- `POST /api/v1/permisos` - Crear permiso

### Grupos de Examen
- `GET /api/v1/grupos-examen` - Listar grupos de examen
- `POST /api/v1/grupos-examen` - Crear grupo de examen

### Asignaciones
- `GET /api/v1/asignaciones-aulas` - Listar asignaciones de aulas
- `GET /api/v1/asignaciones-sinodales` - Listar asignaciones de sinodales
- `POST /api/v1/asignaciones-aulas` - Crear asignación de aula
- `POST /api/v1/asignaciones-sinodales` - Crear asignación de sinodal

---

## Manejo de Errores

La API retorna códigos de estado HTTP estándar:

| Código | Significado | Descripción |
|--------|-------------|-------------|
| `200` | OK | Petición exitosa |
| `201` | Created | Recurso creado exitosamente |
| `400` | Bad Request | Datos inválidos en la petición |
| `401` | Unauthorized | Token faltante o inválido |
| `403` | Forbidden | Sin permisos para este recurso |
| `404` | Not Found | Recurso no encontrado |
| `500` | Internal Server Error | Error del servidor |

**Formato de error:**
```json
{
  "detail": "Descripción del error"
}
```

---

## CORS

El servidor permite peticiones desde los siguientes orígenes:

- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:3001`
- `http://127.0.0.1:3001`

Si necesitas agregar más orígenes, contacta al equipo de backend.

---

## Documentación Interactiva

Una vez que el servidor esté corriendo, puedes acceder a:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Estas interfaces permiten probar todos los endpoints directamente desde el navegador.

---

## Ejemplo Completo - React

```jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

// Interceptor para agregar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

function App() {
  const [user, setUser] = useState(null);
  const [solicitudes, setSolicitudes] = useState([]);

  // Login
  const handleLogin = async (username, password) => {
    try {
      const { data } = await api.post('/auth/login', {
        user: username,
        password: password
      });
      
      localStorage.setItem('token', data.token);
      setUser(data.user);
    } catch (error) {
      console.error('Error en login:', error);
    }
  };

  // Obtener solicitudes
  useEffect(() => {
    if (user) {
      api.get('/solicitudes')
        .then(({ data }) => setSolicitudes(data))
        .catch(console.error);
    }
  }, [user]);

  // Logout
  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <div>
      {!user ? (
        <LoginForm onLogin={handleLogin} />
      ) : (
        <>
          <h1>Bienvenido, {user.nombre_usuario}</h1>
          <button onClick={handleLogout}>Cerrar Sesión</button>
          <SolicitudesList solicitudes={solicitudes} />
        </>
      )}
    </div>
  );
}
```

---

## Notas Importantes

1. **Seguridad:**
   - Nunca expongas el token en la URL
   - Usa HTTPS en producción
   - El token expira en 30 días por defecto
   - No guardes información sensible en localStorage

2. **Tokens:**
   - Los tokens son válidos por 30 días
   - No hay endpoint de refresh token actualmente
   - Al expirar, el usuario debe hacer login nuevamente

3. **Permisos:**
   - Verifica el rol del usuario antes de mostrar opciones en el frontend
   - El backend valida permisos en cada petición
   - Los jefes solo pueden ver/modificar datos de su carrera

---

## Soporte y Documentación Adicional

- **Guía de Instalación:** Ver `docs/QUICKSTART.md`
- **Documentación Completa:** Ver `docs/AUTH_GUIDE.md`
- **Diagramas del Sistema:** Ver `docs/DIAGRAMAS.md`
- **Comandos Útiles:** Ver `docs/COMANDOS.md`

---