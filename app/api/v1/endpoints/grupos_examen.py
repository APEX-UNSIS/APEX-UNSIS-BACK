from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.GrupoExamenRepository import GrupoExamenRepository
from app.schemas.GrupoExamenSchema import GrupoExamen, GrupoExamenCreate, GrupoExamenUpdate
from app.services.GrupoExamenService import GrupoExamenService

router = APIRouter(prefix="/grupos-examen", tags=["grupos-examen"])


def get_grupo_examen_service(db: Session = Depends(get_db)) -> GrupoExamenService:
    repository = GrupoExamenRepository(db)
    return GrupoExamenService(repository)


@router.get("/", response_model=List[GrupoExamen])
def read_grupos_examen(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: GrupoExamenService = Depends(get_grupo_examen_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{id_examen_grupo}", response_model=GrupoExamen)
def read_grupo_examen(
    id_examen_grupo: str,
    service: GrupoExamenService = Depends(get_grupo_examen_service)
):
    grupo = service.get(id_examen_grupo)
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo de examen no encontrado")
    return grupo


@router.get("/solicitud/{id_horario}", response_model=List[GrupoExamen])
def read_grupos_examen_por_solicitud(
    id_horario: str,
    service: GrupoExamenService = Depends(get_grupo_examen_service)
):
    return service.get_by_solicitud(id_horario)


@router.get("/grupo/{id_grupo}", response_model=List[GrupoExamen])
def read_grupos_examen_por_grupo(
    id_grupo: str,
    service: GrupoExamenService = Depends(get_grupo_examen_service)
):
    return service.get_by_grupo(id_grupo)


@router.post("/", response_model=GrupoExamen)
def create_grupo_examen(
    grupo: GrupoExamenCreate,
    service: GrupoExamenService = Depends(get_grupo_examen_service)
):
    return service.create(grupo)


@router.put("/{id_examen_grupo}", response_model=GrupoExamen)
def update_grupo_examen(
    id_examen_grupo: str,
    grupo_update: GrupoExamenUpdate,
    service: GrupoExamenService = Depends(get_grupo_examen_service)
):
    grupo = service.update(id_examen_grupo, grupo_update)
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo de examen no encontrado")
    return grupo


@router.delete("/{id_examen_grupo}", response_model=GrupoExamen)
def delete_grupo_examen(
    id_examen_grupo: str,
    service: GrupoExamenService = Depends(get_grupo_examen_service)
):
    grupo = service.delete(id_examen_grupo)
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo de examen no encontrado")
    return grupo