from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.PermisoRepository import PermisoRepository
from app.schemas.PermisoSinodalSchema import PermisoSinodal, PermisoSinodalCreate, PermisoSinodalUpdate
from app.services.PermisoService import PermisoService

router = APIRouter(prefix="/permisos", tags=["permisos"])


def get_permiso_service(db: Session = Depends(get_db)) -> PermisoService:
    repository = PermisoRepository(db)
    return PermisoService(repository)


@router.get("/", response_model=List[PermisoSinodal])
def read_permisos(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        service: PermisoService = Depends(get_permiso_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{id_regla}", response_model=PermisoSinodal)
def read_permiso(
        id_regla: str,
        service: PermisoService = Depends(get_permiso_service)
):
    permiso = service.get(id_regla)
    if permiso is None:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return permiso


@router.get("/profesor/{id_profesor}", response_model=List[PermisoSinodal])
def read_permisos_por_profesor(
        id_profesor: str,
        service: PermisoService = Depends(get_permiso_service)
):
    return service.get_by_profesor(id_profesor)


@router.get("/materia/{id_materia}", response_model=List[PermisoSinodal])
def read_permisos_por_materia(
        id_materia: str,
        service: PermisoService = Depends(get_permiso_service)
):
    return service.get_by_materia(id_materia)


@router.post("/", response_model=PermisoSinodal)
def create_permiso(
        permiso: PermisoSinodalCreate,
        service: PermisoService = Depends(get_permiso_service)
):
    # Check if permiso already exists
    existing = service.get_by_profesor_materia(permiso.id_profesor, permiso.id_materia)
    if existing:
        raise HTTPException(status_code=400, detail="Permiso ya existe para este profesor y materia")
    return service.create(permiso)


@router.put("/{id_regla}", response_model=PermisoSinodal)
def update_permiso(
        id_regla: str,
        permiso_update: PermisoSinodalUpdate,
        service: PermisoService = Depends(get_permiso_service)
):
    permiso = service.update(id_regla, permiso_update)
    if permiso is None:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return permiso


@router.delete("/{id_regla}", response_model=PermisoSinodal)
def delete_permiso(
        id_regla: str,
        service: PermisoService = Depends(get_permiso_service)
):
    permiso = service.delete(id_regla)
    if permiso is None:
        raise HTTPException(status_code=404, detail="Permiso no encontrado")
    return permiso