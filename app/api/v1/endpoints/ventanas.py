from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.VentanaRepository import VentanaRepository
from app.schemas.VentanaAplicacionSchema import VentanaAplicacion, VentanaAplicacionCreate, VentanaAplicacionUpdate
from app.services.VentanaService import VentanaService

router = APIRouter(prefix="/ventanas", tags=["ventanas"])


def get_ventana_service(db: Session = Depends(get_db)) -> VentanaService:
    repository = VentanaRepository(db)
    return VentanaService(repository)


@router.get("/", response_model=List[VentanaAplicacion])
def read_ventanas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: VentanaService = Depends(get_ventana_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{id_ventana}", response_model=VentanaAplicacion)
def read_ventana(
    id_ventana: str,
    service: VentanaService = Depends(get_ventana_service)
):
    ventana = service.get(id_ventana)
    if ventana is None:
        raise HTTPException(status_code=404, detail="Ventana no encontrada")
    return ventana


@router.get("/periodo/{id_periodo}/evaluacion/{id_evaluacion}", response_model=VentanaAplicacion)
def read_ventana_por_periodo_evaluacion(
    id_periodo: str,
    id_evaluacion: str,
    service: VentanaService = Depends(get_ventana_service)
):
    ventana = service.get_by_periodo_evaluacion(id_periodo, id_evaluacion)
    if ventana is None:
        raise HTTPException(status_code=404, detail="Ventana no encontrada")
    return ventana


@router.post("/", response_model=VentanaAplicacion)
def create_ventana(
    ventana: VentanaAplicacionCreate,
    service: VentanaService = Depends(get_ventana_service)
):
    return service.create(ventana)


@router.put("/{id_ventana}", response_model=VentanaAplicacion)
def update_ventana(
    id_ventana: str,
    ventana_update: VentanaAplicacionUpdate,
    service: VentanaService = Depends(get_ventana_service)
):
    ventana = service.update(id_ventana, ventana_update)
    if ventana is None:
        raise HTTPException(status_code=404, detail="Ventana no encontrada")
    return ventana


@router.delete("/{id_ventana}", response_model=VentanaAplicacion)
def delete_ventana(
    id_ventana: str,
    service: VentanaService = Depends(get_ventana_service)
):
    ventana = service.delete(id_ventana)
    if ventana is None:
        raise HTTPException(status_code=404, detail="Ventana no encontrada")
    return ventana