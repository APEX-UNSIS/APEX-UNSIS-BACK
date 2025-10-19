# APEX-UNSIS

Sistema de gestión de horarios de exámenes desarrollado con Django REST Framework y PostgreSQL.

## Características

- **Backend**: Django REST Framework
- **Base de datos**: PostgreSQL
- **Contenedores**: Docker y Docker Compose
- **API REST**: Para gestión de horarios de exámenes

## Modelos principales

- **Periodo**: Gestión de periodos académicos
- **TipoEvaluacion**: Tipos de evaluaciones/exámenes
- **Grupo**: Grupos de estudiantes
- **Materia**: Materias académicas
- **Profesor**: Profesores y sinodales
- **Aula**: Aulas disponibles
- **HorarioExamen**: Horarios de exámenes (modelo central)

## Instalación con Docker

### Prerrequisitos
- Docker
- Docker Compose

### Pasos para ejecutar

1. **Clonar el repositorio**
```bash
git clone <url-del-repo>
cd APEX-UNSIS
```

2. **Levantar los contenedores**
```bash
docker-compose up -d --build
```

3. **Ejecutar migraciones**
```bash
docker-compose exec web python manage.py migrate
```

4. **Crear superusuario**
```bash
docker-compose exec web python manage.py createsuperuser
```

### Acceso a servicios

- **Backend Django**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin
- **PostgreSQL**: localhost:5433
  - Usuario: `postgres`
  - Contraseña: `root`
  - Base de datos: `apexunsisdb`

## Comandos útiles

```bash
# Ver logs
docker-compose logs -f

# Acceder al contenedor web
docker-compose exec web bash

# Acceder a PostgreSQL
docker-compose exec db psql -U postgres -d apexunsisdb

# Parar contenedores
docker-compose down

# Parar y eliminar volúmenes
docker-compose down -v
```

## Estructura del proyecto

```
APEX-UNSIS/
├── apexunsis/          # Configuración principal Django
├── apexunsisapi/       # App principal con modelos y API
├── docker-compose.yml  # Configuración Docker
├── Dockerfile          # Imagen del backend
├── requirements.txt    # Dependencias Python
└── manage.py          # CLI de Django
```

## Desarrollo

Para desarrollo local, los cambios en el código se reflejan automáticamente gracias al volumen montado en Docker.
