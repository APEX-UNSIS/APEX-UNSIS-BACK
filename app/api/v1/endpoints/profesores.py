from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.ProfesorRepository import ProfesorRepository
from app.schemas.ProfesorSchema import Profesor, ProfesorCreate, ProfesorUpdate
from app.services.ProfesorService import ProfesorService

router = APIRouter(prefix="/profesores", tags=["profesores"])


def get_profesor_service(db: Session = Depends(get_db)) -> ProfesorService:
    repository = ProfesorRepository(db)
    return ProfesorService(repository)


@router.get("/", response_model=List[Profesor])
def read_profesores(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        service: ProfesorService = Depends(get_profesor_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/activos", response_model=List[Profesor])
def read_profesores_activos(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        service: ProfesorService = Depends(get_profesor_service)
):
    return service.get_activos(skip=skip, limit=limit)


@router.get("/{id_profesor}", response_model=Profesor)
def read_profesor(
        id_profesor: str,
        service: ProfesorService = Depends(get_profesor_service)
):
    profesor = service.get(id_profesor)
    if profesor is None:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor


@router.post("/", response_model=Profesor)
def create_profesor(
        profesor: ProfesorCreate,
        service: ProfesorService = Depends(get_profesor_service)
):
    return service.create(profesor)


@router.put("/{id_profesor}", response_model=Profesor)
def update_profesor(
        id_profesor: str,
        profesor_update: ProfesorUpdate,
        service: ProfesorService = Depends(get_profesor_service)
):
    profesor = service.update(id_profesor, profesor_update)
    if profesor is None:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor


@router.delete("/{id_profesor}", response_model=Profesor)
def delete_profesor(
        id_profesor: str,
        service: ProfesorService = Depends(get_profesor_service)
):
    profesor = service.delete(id_profesor)
    if profesor is None:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor