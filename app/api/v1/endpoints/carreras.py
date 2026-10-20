from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.CarreraRepository import CarreraRepository
from app.schemas.CarreraSchema import Carrera, CarreraCreate, CarreraUpdate
from app.services.CarreraService import CarreraService

router = APIRouter(prefix="/carreras", tags=["carreras"])


def get_carrera_service(db: Session = Depends(get_db)) -> CarreraService:
    repository = CarreraRepository(db)
    return CarreraService(repository)


@router.get("/", response_model=List[Carrera])
def read_carreras(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: CarreraService = Depends(get_carrera_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{id_carrera}", response_model=Carrera)
def read_carrera(
    id_carrera: str,
    service: CarreraService = Depends(get_carrera_service)
):
    carrera = service.get(id_carrera)
    if carrera is None:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera


@router.post("/", response_model=Carrera)
def create_carrera(
    carrera: CarreraCreate,
    service: CarreraService = Depends(get_carrera_service)
):
    # Check if carrera already exists
    existing = service.get_by_nombre(carrera.nombre_carrera)
    if existing:
        raise HTTPException(status_code=400, detail="Carrera ya existe")
    return service.create(carrera)


@router.put("/{id_carrera}", response_model=Carrera)
def update_carrera(
    id_carrera: str,
    carrera_update: CarreraUpdate,
    service: CarreraService = Depends(get_carrera_service)
):
    carrera = service.update(id_carrera, carrera_update)
    if carrera is None:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera


@router.delete("/{id_carrera}", response_model=Carrera)
def delete_carrera(
    id_carrera: str,
    service: CarreraService = Depends(get_carrera_service)
):
    carrera = service.delete(id_carrera)
    if carrera is None:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera


@router.get("/search/", response_model=List[Carrera])
def search_carreras(
    nombre: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: CarreraService = Depends(get_carrera_service)
):
    return service.search_by_nombre(nombre, skip=skip, limit=limit)