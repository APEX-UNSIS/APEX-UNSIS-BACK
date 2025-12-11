from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.AsignacionSinodalRepository import AsignacionSinodalRepository
from app.schemas.AsignacionSinodalSchema import AsignacionSinodal, AsignacionSinodalCreate, AsignacionSinodalUpdate
from app.services.AsignacionSinodalService import AsignacionSinodalService

router = APIRouter(prefix="/asignaciones-sinodales", tags=["asignaciones-sinodales"])


def get_asignacion_sinodal_service(db: Session = Depends(get_db)) -> AsignacionSinodalService:
    repository = AsignacionSinodalRepository(db)
    return AsignacionSinodalService(repository)


@router.get("/", response_model=List[AsignacionSinodal])
def read_asignaciones_sinodales(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: AsignacionSinodalService = Depends(get_asignacion_sinodal_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{id_examen_sinodal}", response_model=AsignacionSinodal)
def read_asignacion_sinodal(
    id_examen_sinodal: str,
    service: AsignacionSinodalService = Depends(get_asignacion_sinodal_service)
):
    asignacion = service.get(id_examen_sinodal)
    if asignacion is None:
        raise HTTPException(status_code=404, detail="Asignación de sinodal no encontrada")
    return asignacion


@router.get("/solicitud/{id_horario}", response_model=List[AsignacionSinodal])
def read_asignaciones_sinodales_por_solicitud(
    id_horario: str,
    service: AsignacionSinodalService = Depends(get_asignacion_sinodal_service)
):
    return service.get_by_solicitud(id_horario)


@router.get("/profesor/{id_profesor}", response_model=List[AsignacionSinodal])
def read_asignaciones_sinodales_por_profesor(
    id_profesor: str,
    service: AsignacionSinodalService = Depends(get_asignacion_sinodal_service)
):
    return service.get_by_profesor(id_profesor)


@router.post("/", response_model=AsignacionSinodal)
def create_asignacion_sinodal(
    asignacion: AsignacionSinodalCreate,
    service: AsignacionSinodalService = Depends(get_asignacion_sinodal_service)
):
    return service.create(asignacion)


@router.put("/{id_examen_sinodal}", response_model=AsignacionSinodal)
def update_asignacion_sinodal(
    id_examen_sinodal: str,
    asignacion_update: AsignacionSinodalUpdate,
    service: AsignacionSinodalService = Depends(get_asignacion_sinodal_service)
):
    asignacion = service.update(id_examen_sinodal, asignacion_update)
    if asignacion is None:
        raise HTTPException(status_code=404, detail="Asignación de sinodal no encontrada")
    return asignacion


@router.delete("/{id_examen_sinodal}", response_model=AsignacionSinodal)
def delete_asignacion_sinodal(
    id_examen_sinodal: str,
    service: AsignacionSinodalService = Depends(get_asignacion_sinodal_service)
):
    asignacion = service.delete(id_examen_sinodal)
    if asignacion is None:
        raise HTTPException(status_code=404, detail="Asignación de sinodal no encontrada")
    return asignacion