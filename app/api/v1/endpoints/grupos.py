from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.GrupoRepository import GrupoRepository
from app.schemas.GrupoEscolarSchema import GrupoEscolar, GrupoEscolarCreate, GrupoEscolarUpdate
from app.services.GrupoService import GrupoService

router = APIRouter(prefix="/grupos", tags=["grupos"])


def get_grupo_service(db: Session = Depends(get_db)) -> GrupoService:
    repository = GrupoRepository(db)
    return GrupoService(repository)


@router.get("/", response_model=List[GrupoEscolar])
def read_grupos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: GrupoService = Depends(get_grupo_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{id_grupo}", response_model=GrupoEscolar)
def read_grupo(
    id_grupo: str,
    service: GrupoService = Depends(get_grupo_service)
):
    grupo = service.get(id_grupo)
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo


@router.get("/{id_grupo}/completo", response_model=GrupoEscolar)
def read_grupo_completo(
    id_grupo: str,
    service: GrupoService = Depends(get_grupo_service)
):
    grupo = service.get_with_carrera(id_grupo)
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo


@router.get("/carrera/{id_carrera}", response_model=List[GrupoEscolar])
def read_grupos_por_carrera(
    id_carrera: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: GrupoService = Depends(get_grupo_service)
):
    return service.get_by_carrera(id_carrera, skip=skip, limit=limit)


@router.post("/", response_model=GrupoEscolar)
def create_grupo(
    grupo: GrupoEscolarCreate,
    service: GrupoService = Depends(get_grupo_service)
):
    return service.create(grupo)


@router.put("/{id_grupo}", response_model=GrupoEscolar)
def update_grupo(
    id_grupo: str,
    grupo_update: GrupoEscolarUpdate,
    service: GrupoService = Depends(get_grupo_service)
):
    grupo = service.update(id_grupo, grupo_update)
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo


@router.delete("/{id_grupo}", response_model=GrupoEscolar)
def delete_grupo(
    id_grupo: str,
    service: GrupoService = Depends(get_grupo_service)
):
    grupo = service.delete(id_grupo)
    if grupo is None:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return grupo