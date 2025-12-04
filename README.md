# Apex Backend

API REST construida con FastAPI.

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd apex-backend
```

### 2. Crear entorno virtual

```bash
python3 -m venv venv
```

### 3. Activar el entorno virtual

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 🏃 Ejecutar el Proyecto

### Modo desarrollo (con auto-reload)

```bash
fastapi dev
```

O alternativamente:

```bash
uvicorn app.main:app --reload
```

### Modo producción

```bash
fastapi run
```

O:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📂 Estructura del Proyecto

```
apex-backend/
├── app/
│   ├── __init__.py
│   └── main.py          # Aplicación principal FastAPI
├── venv/                # Entorno virtual (no versionado)
├── .gitignore
├── requirements.txt     # Dependencias del proyecto
└── README.md
```

## 🔍 Endpoints Disponibles

### Documentación Interactiva

Una vez ejecutado el servidor, accede a:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Endpoints de la API

- `GET /` - Mensaje de bienvenida
- `GET /saludo/{nombre}` - Saludo personalizado

## 🛠️ Comandos Útiles

### Ver dependencias instaladas

```bash
pip list
```

### Actualizar requirements.txt

```bash
pip freeze > requirements.txt
```

### Desactivar entorno virtual

```bash
deactivate
```

## 📦 Tecnologías

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno y rápido
- [Uvicorn](https://www.uvicorn.org/) - Servidor ASGI de alto rendimiento
- [Python 3.13](https://www.python.org/) - Lenguaje de programación

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

## 📝 Notas

- El entorno virtual (`venv/`) no se versiona en Git
- Asegúrate de tener el entorno virtual activado antes de instalar dependencias
- En producción, configura correctamente CORS en `app/main.py`

## 📄 Licencia

[Especifica tu licencia aquí]
