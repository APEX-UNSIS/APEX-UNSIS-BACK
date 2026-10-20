"""
Registro central de routers de la API v1.

Cada feature expone su router en `app.features.<feature>.interfaces.router`
(a excepción de auth, que vive en `app.features.usuarios.interfaces.auth`).
"""
from fastapi import APIRouter

from app.features.carreras.interfaces.router import router as carreras_router
from app.features.periodos.interfaces.router import router as periodos_router
from app.features.evaluaciones.interfaces.router import router as evaluaciones_router
from app.features.materias.interfaces.router import router as materias_router
from app.features.profesores.interfaces.router import router as profesores_router
from app.features.aulas.interfaces.router import router as aulas_router
from app.features.grupos.interfaces.router import router as grupos_router
from app.features.horarios.interfaces.router import router as horarios_router
from app.features.permisos.interfaces.router import router as permisos_router
from app.features.ventanas.interfaces.router import router as ventanas_router
from app.features.solicitudes.interfaces.router import router as solicitudes_router
from app.features.grupos_examen.interfaces.router import router as grupos_examen_router
from app.features.asignaciones_aulas.interfaces.router import router as asignaciones_aulas_router
from app.features.asignaciones_sinodales.interfaces.router import router as asignaciones_sinodales_router
from app.features.usuarios.interfaces.auth import router as auth_router
from app.features.usuarios.interfaces.router import router as usuarios_router
from app.features.calendario.interfaces.router import router as calendario_router
from app.features.admin.interfaces.router import router as admin_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(usuarios_router)
api_router.include_router(carreras_router)
api_router.include_router(periodos_router)
api_router.include_router(evaluaciones_router)
api_router.include_router(materias_router)
api_router.include_router(profesores_router)
api_router.include_router(aulas_router)
api_router.include_router(grupos_router)
api_router.include_router(horarios_router)
api_router.include_router(permisos_router)
api_router.include_router(ventanas_router)
api_router.include_router(solicitudes_router)
api_router.include_router(grupos_examen_router)
api_router.include_router(asignaciones_aulas_router)
api_router.include_router(asignaciones_sinodales_router)
api_router.include_router(calendario_router)
api_router.include_router(admin_router)
