from fastapi import APIRouter

from app.api.v1.endpoints import carreras, periodos, evaluaciones, materias, profesores, aulas, grupos, horarios, \
    permisos, ventanas, solicitudes, grupos_examen, asignaciones_aulas, asignaciones_sinodales, auth, usuarios, calendario, admin

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(usuarios.router)
api_router.include_router(carreras.router)
api_router.include_router(periodos.router)
api_router.include_router(evaluaciones.router)
api_router.include_router(materias.router)
api_router.include_router(profesores.router)
api_router.include_router(aulas.router)
api_router.include_router(grupos.router)
api_router.include_router(horarios.router)
api_router.include_router(permisos.router)
api_router.include_router(ventanas.router)
api_router.include_router(solicitudes.router)
api_router.include_router(grupos_examen.router)
api_router.include_router(asignaciones_aulas.router)
api_router.include_router(asignaciones_sinodales.router)
api_router.include_router(calendario.router)
api_router.include_router(admin.router)