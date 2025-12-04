# Apex Backend

> API REST construida con **FastAPI** - Rápida, moderna y lista para producción.

---

## Requisitos Previos

Asegúrate de tener instalado:

- **Python** 3.8 o superior
- **pip** (gestor de paquetes de Python)
- **Git**

> [!TIP]
> Verifica tu versión de Python ejecutando: `python3 --version`

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd apex-backend
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
```

> [!NOTE]
> El entorno virtual mantiene las dependencias aisladas del sistema.

### 3. Activar el entorno virtual

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

> [!IMPORTANT]
> Siempre activa el entorno virtual antes de trabajar en el proyecto.

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecutar el Proyecto

### Modo desarrollo (con auto-reload)

```bash
fastapi dev
```

**Alternativa con Uvicorn:**
```bash
uvicorn app.main:app --reload
```

> [!TIP]
> El flag `--reload` reinicia automáticamente el servidor cuando detecta cambios en el código.

### Modo producción

```bash
fastapi run
```

**Alternativa con Uvicorn:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

> [!WARNING]
> No uses `--reload` en producción, consume recursos adicionales.

---

## Estructura del Proyecto

```
apex-backend/
├── app/
│   ├── __init__.py
│   └── main.py          # 🚀 Aplicación principal FastAPI
├── venv/                # 📦 Entorno virtual (no versionado)
├── .gitignore           # 🚫 Archivos ignorados por Git
├── requirements.txt     # 📋 Dependencias del proyecto
└── README.md            # 📖 Documentación
```

> [!NOTE]
> La carpeta `venv/` no se sube a Git gracias al archivo `.gitignore`.

---

## Endpoints Disponibles

### Documentación Interactiva

Una vez ejecutado el servidor, accede a:

| Documentación | URL |
|---------------|-----|
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |

> [!TIP]
> FastAPI genera documentación interactiva automáticamente. Puedes probar los endpoints directamente desde Swagger UI.

### Endpoints de la API

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Mensaje de bienvenida |
| `GET` | `/saludo/{nombre}` | Saludo personalizado |

---

## Comandos Útiles

| Comando | Descripción |
|---------|-------------|
| `pip list` | Ver todas las dependencias instaladas |
| `pip freeze > requirements.txt` | Actualizar archivo de dependencias |
| `deactivate` | Desactivar el entorno virtual |
| `pip install --upgrade pip` | Actualizar pip a la última versión |

> [!TIP]
> Ejecuta `pip freeze > requirements.txt` después de instalar nuevos paquetes para mantener actualizado el archivo de dependencias.

---

## Tecnologías

<div align="center">

| Tecnología | Descripción |
|------------|-------------|
| [**FastAPI**](https://fastapi.tiangolo.com/) | Framework web moderno y rápido |
| [**Uvicorn**](https://www.uvicorn.org/) | Servidor ASGI de alto rendimiento |
| [**Python 3.13**](https://www.python.org/) | Lenguaje de programación |

</div>

> [!NOTE]
> FastAPI está construido sobre estándares modernos como OpenAPI y JSON Schema.

---

## Contribuir

¿Quieres contribuir? ¡Genial! Sigue estos pasos:

1. **Fork** el proyecto
2. Crea una **rama** para tu feature:
   ```bash
   git checkout -b feature/NuevaCaracteristica
   ```
3. **Commit** tus cambios:
   ```bash
   git commit -m 'Añadir nueva característica'
   ```
4. **Push** a la rama:
   ```bash
   git push origin feature/NuevaCaracteristica
   ```
5. Abre un **Pull Request**

> [!IMPORTANT]
> Asegúrate de que tu código pase todas las pruebas antes de crear un Pull Request.

---

## Notas

> [!CAUTION]
> En producción, **NO** uses `allow_origins=["*"]` en CORS. Especifica los dominios permitidos explícitamente.

**Recordatorios importantes:**
-  El entorno virtual (`venv/`) no se versiona en Git
-  Activa siempre el entorno virtual antes de instalar dependencias
-  Revisa la configuración de CORS en `app/main.py` para producción
-  Usa variables de entorno para configuración sensible

---

## Licencia

[Especifica tu licencia aquí]

---

<div align="center">


</div>
