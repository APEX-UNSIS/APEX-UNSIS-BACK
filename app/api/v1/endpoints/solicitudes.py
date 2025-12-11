from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.SolicitudRepository import SolicitudRepository
from app.schemas.EstadoSolicitudSchema import EstadoSolicitud
from app.schemas.SolicitudExamenSchema import SolicitudExamen, SolicitudExamenCreate, SolicitudExamenUpdate
from app.services.SolicitudService import SolicitudService

router = APIRouter(prefix="/solicitudes", tags=["solicitudes"])


def get_solicitud_service(db: Session = Depends(get_db)) -> SolicitudService:
    repository = SolicitudRepository(db)
    return SolicitudService(repository)


@router.get("/", response_model=List[SolicitudExamen])
def read_solicitudes(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        service: SolicitudService = Depends(get_solicitud_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{id_horario}", response_model=SolicitudExamen)
def read_solicitud(
        id_horario: str,
        service: SolicitudService = Depends(get_solicitud_service)
):
    solicitud = service.get(id_horario)
    if solicitud is None:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud


@router.get("/estado/{estado}", response_model=List[SolicitudExamen])
def read_solicitudes_por_estado(
        estado: EstadoSolicitud,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        service: SolicitudService = Depends(get_solicitud_service)
):
    return service.get_by_estado(estado, skip=skip, limit=limit)


@router.get("/fecha/{fecha}", response_model=List[SolicitudExamen])
def read_solicitudes_por_fecha(
        fecha: date,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        service: SolicitudService = Depends(get_solicitud_service)
):
    return service.get_by_fecha(fecha, skip=skip, limit=limit)


@router.get("/periodo/{id_periodo}", response_model=List[SolicitudExamen])
def read_solicitudes_por_periodo(
        id_periodo: str,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        service: SolicitudService = Depends(get_solicitud_service)
):
    return service.get_by_periodo(id_periodo, skip=skip, limit=limit)


@router.post("/", response_model=SolicitudExamen)
def create_solicitud(
        solicitud: SolicitudExamenCreate,
        service: SolicitudService = Depends(get_solicitud_service)
):
    return service.create(solicitud)


@router.put("/{id_horario}", response_model=SolicitudExamen)
def update_solicitud(
        id_horario: str,
        solicitud_update: SolicitudExamenUpdate,
        service: SolicitudService = Depends(get_solicitud_service)
):
    solicitud = service.update(id_horario, solicitud_update)
    if solicitud is None:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud


@router.delete("/{id_horario}", response_model=SolicitudExamen)
def delete_solicitud(
        id_horario: str,
        service: SolicitudService = Depends(get_solicitud_service)
):
    solicitud = service.delete(id_horario)
    if solicitud is None:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return solicitud


@router.post("/{id_horario}/aprobar", response_model=SolicitudExamen)
def aprobar_solicitud(
        id_horario: str,
        service: SolicitudService = Depends(get_solicitud_service)
):
    solicitud = service.get(id_horario)
    if solicitud is None:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    update_data = SolicitudExamenUpdate(estado=EstadoSolicitud.APROBADO, motivo_rechazo=None)
    return service.update(id_horario, update_data)


@router.post("/{id_horario}/rechazar", response_model=SolicitudExamen)
def rechazar_solicitud(
        id_horario: str,
        motivo: str = Query(..., description="Motivo del rechazo"),
        service: SolicitudService = Depends(get_solicitud_service)
):
    solicitud = service.get(id_horario)
    if solicitud is None:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")

    update_data = SolicitudExamenUpdate(estado=EstadoSolicitud.RECHAZADO, motivo_rechazo=motivo)
    return service.update(id_horario, update_data)