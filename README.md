# API REST - APEX UNSIS Backend

Backend en **FastAPI + PostgreSQL** de APEX (UNSIS): sistema de gestión del proceso de
exámenes profesionales —carreras, materias, grupos, horarios, aulas, solicitudes de examen,
sinodales y generación del calendario de exámenes— con autenticación JWT y roles
(`admin`, `jefe`, `servicios`).

> [!NOTE]
> La documentación detallada vive en [`Docs/`](Docs/INDICE.md):
> [instalación](Docs/QUICKSTART.md) · [referencia de la API](Docs/API_REFERENCE.md) ·
> [autenticación](Docs/AUTH_GUIDE.md) · [diagramas](Docs/DIAGRAMAS.md).
> Con el servidor corriendo, Swagger está en `http://localhost:8000/docs`.

---

## Requisitos

- Python 3.12+
- PostgreSQL
- (opcional) Docker

## Arranque rápido

```bash
git clone <repo-url>
cp .env.example .env      # completar credenciales de la base de datos
pip install -r requirements.txt
uvicorn app.main:app --reload
```

> [!WARNING]
> La aplicación no arranca sin un `.env` completo: `DB_HOST`, `DB_USER`,
> `DB_PASSWORD` y `DB_NAME` son obligatorias.

---

## Arquitectura hexagonal por features (release 2.0)

Cada dominio del sistema es una **feature** autosuficiente organizada en tres capas:

```text
app/
├── core/                  # bases compartidas (BaseRepository, BaseService)
├── api/v1/                # registro único de routers
└── features/              # 17 features, una por entidad
    └── <feature>/
        ├── domain/          # models.py · schemas.py · service.py
        ├── infrastructure/  # repository.py
        └── interfaces/      # router.py
```

> [!TIP]
> **Regla de dependencias:** `interfaces → infrastructure → domain → core`.
> Nunca importes "hacia atrás" ni cruces features por debajo de sus `interfaces`.
> Para exponer un nuevo recurso, crea su carpeta en `app/features/<feature>/`.

---

## Flujo de trabajo: Git Flow

| Flujo | Rama | Uso |
|-------|------|-----|
| develop | `dev` | integración del trabajo diario (pausado por realese2.0) |
| release 2.0 | `realese2.0-dev` | reestructuración de arquitectura (en curso) |
| main | `main` | producción |

> [!WARNING]
> Usa los nombres **exactos** de la tabla: la rama de desarrollo es `dev`
> (no `develop`) y `realese2.0-dev` conserva un typo histórico ya propagado
> en el remoto.

Cómo se trabaja:

1. Las funcionalidades se desarrollan en `feature/<nombre>` partiendo de `dev`.
2. Se abre un PR contra `dev`: revisión de código + commits convencionales.
3. Al preparar una release se crea `release/<version>` → se prueba → merge a `main` con tag
   → y se reintegra a `dev`.
4. Los arreglos urgentes de producción salen como `hotfix/<nombre>` desde `main`.

> [!TIP]
> El trabajo de reestructuración actual vive en `refact/architecture`
> y se integra en `realese2.0-dev`.

---

## Commits: Conventional Commits

Formato: `<tipo>(<scope>): <descripción corta>`

| Tipo | Cuándo se usa |
|------|---------------|
| `feat` | nueva funcionalidad |
| `fix` | corrección de un bug |
| `refactor` | reestructurar código sin cambiar comportamiento |
| `docs` | documentación |
| `test` | pruebas |
| `build` / `ci` | dependencias, Docker, pipelines |
| `chore` | mantenimiento (limpieza, tooling) |

Ejemplos reales de este repositorio:

```text
feat(generar-calendario-v3): back con solo crear_tablas y reset admin
refactor(features): repositories en infrastructure y services en domain
docs: readme con introduccion y flujo de trabajo
```

> [!TIP]
> Un commit = una intención. El `scope` (área o feature) es opcional pero
> recomendado; el mensaje va en minúsculas y sin punto final.

---

## Documentación

| Guía | Contenido |
|------|-----------|
| [Docs/QUICKSTART.md](Docs/QUICKSTART.md) | Instalación y arranque en 5 min |
| [Docs/API_REFERENCE.md](Docs/API_REFERENCE.md) | Endpoints, errores y ejemplos de frontend |
| [Docs/AUTH_GUIDE.md](Docs/AUTH_GUIDE.md) | Autenticación y roles en detalle |
| [Docs/DIAGRAMAS.md](Docs/DIAGRAMAS.md) | Diagramas del sistema |
| [Docs/COMANDOS.md](Docs/COMANDOS.md) | Comandos útiles |
| [Docs/INDICE.md](Docs/INDICE.md) | Índice completo de la documentación |


### Comandos utiles para docker 
```bash
cp .env.example .env          # ajustar SECRET_KEY y credenciales
docker compose up -d --build
docker compose logs -f backend  # ver logs de arranque       
``` 

#### al levantar con compose debe marcar creados y corriendo lo siguiente
```bash
[+] up 5/5
 ✔ Image apex-unsis-backend       Built                                    31.9s
 ✔ Image apex-unsis-front         Built                                    32.0s
 ✔ Container apex-unsis-front-1   Running                                   0.0s
 ✔ Container apex-unsis-db-1      Healthy                                   3.3s
 ✔ Container apex-unsis-backend-1 Healthy 
```