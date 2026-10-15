from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.AulaRepository import AulaRepository
from app.schemas.AulaSchema import Aula, AulaCreate, AulaUpdate
from app.services.AulaService import AulaService

router = APIRouter(prefix="/aulas", tags=["aulas"])


def get_aula_service(db: Session = Depends(get_db)) -> AulaService:
    repository = AulaRepository(db)
    return AulaService(repository)


@router.get("/", response_model=List[Aula])
def read_aulas(
    skip: int = Query(0, ge=0),
    limit: int = Query(500, ge=1, le=2000),
    service: AulaService = Depends(get_aula_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/disponibles", response_model=List[Aula])
def read_aulas_disponibles(
    capacidad_minima: Optional[int] = Query(None, ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(500, ge=1, le=2000),
    service: AulaService = Depends(get_aula_service)
):
    return service.get_disponibles(capacidad_minima, skip=skip, limit=limit)


@router.get("/{id_aula}", response_model=Aula)
def read_aula(
    id_aula: str,
    service: AulaService = Depends(get_aula_service)
):
    aula = service.get(id_aula)
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return aula


@router.post("/", response_model=Aula)
def create_aula(
    aula: AulaCreate,
    service: AulaService = Depends(get_aula_service)
):
    return service.create(aula)


@router.put("/{id_aula}", response_model=Aula)
def update_aula(
    id_aula: str,
    aula_update: AulaUpdate,
    service: AulaService = Depends(get_aula_service)
):
    aula = service.update(id_aula, aula_update)
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return aula


@router.delete("/{id_aula}", response_model=Aula)
def delete_aula(
    id_aula: str,
    service: AulaService = Depends(get_aula_service)
):
    aula = service.delete(id_aula)
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return aula