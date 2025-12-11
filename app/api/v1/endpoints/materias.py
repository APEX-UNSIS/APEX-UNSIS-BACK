from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.MateriaRepository import MateriaRepository
from app.schemas.MateriaSchema import Materia, MateriaCreate, MateriaUpdate
from app.services.MateriaService import MateriaService

router = APIRouter(prefix="/materias", tags=["materias"])


def get_materia_service(db: Session = Depends(get_db)) -> MateriaService:
    repository = MateriaRepository(db)
    return MateriaService(repository)


@router.get("/", response_model=List[Materia])
def read_materias(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: MateriaService = Depends(get_materia_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{id_materia}", response_model=Materia)
def read_materia(
    id_materia: str,
    service: MateriaService = Depends(get_materia_service)
):
    materia = service.get(id_materia)
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia


@router.post("/", response_model=Materia)
def create_materia(
    materia: MateriaCreate,
    service: MateriaService = Depends(get_materia_service)
):
    return service.create(materia)


@router.put("/{id_materia}", response_model=Materia)
def update_materia(
    id_materia: str,
    materia_update: MateriaUpdate,
    service: MateriaService = Depends(get_materia_service)
):
    materia = service.update(id_materia, materia_update)
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia


@router.delete("/{id_materia}", response_model=Materia)
def delete_materia(
    id_materia: str,
    service: MateriaService = Depends(get_materia_service)
):
    materia = service.delete(id_materia)
    if materia is None:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia