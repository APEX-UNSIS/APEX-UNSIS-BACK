from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.AsignacionAulaRepository import AsignacionAulaRepository
from app.schemas.AsignacionAulaSchema import AsignacionAula, AsignacionAulaCreate, AsignacionAulaUpdate
from app.services.AsignacionAulaService import AsignacionAulaService

router = APIRouter(prefix="/asignaciones-aulas", tags=["asignaciones-aulas"])


def get_asignacion_aula_service(db: Session = Depends(get_db)) -> AsignacionAulaService:
    repository = AsignacionAulaRepository(db)
    return AsignacionAulaService(repository)


@router.get("/", response_model=List[AsignacionAula])
def read_asignaciones_aulas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: AsignacionAulaService = Depends(get_asignacion_aula_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{id_examen_aula}", response_model=AsignacionAula)
def read_asignacion_aula(
    id_examen_aula: str,
    service: AsignacionAulaService = Depends(get_asignacion_aula_service)
):
    asignacion = service.get(id_examen_aula)
    if asignacion is None:
        raise HTTPException(status_code=404, detail="Asignación de aula no encontrada")
    return asignacion


@router.get("/solicitud/{id_horario}", response_model=List[AsignacionAula])
def read_asignaciones_aulas_por_solicitud(
    id_horario: str,
    service: AsignacionAulaService = Depends(get_asignacion_aula_service)
):
    return service.get_by_solicitud(id_horario)


@router.get("/aula/{id_aula}", response_model=List[AsignacionAula])
def read_asignaciones_aulas_por_aula(
    id_aula: str,
    service: AsignacionAulaService = Depends(get_asignacion_aula_service)
):
    return service.get_by_aula(id_aula)


@router.get("/aplicador/{id_profesor}", response_model=List[AsignacionAula])
def read_asignaciones_aulas_por_aplicador(
    id_profesor: str,
    service: AsignacionAulaService = Depends(get_asignacion_aula_service)
):
    return service.get_by_profesor_aplicador(id_profesor)


@router.post("/", response_model=AsignacionAula)
def create_asignacion_aula(
    asignacion: AsignacionAulaCreate,
    service: AsignacionAulaService = Depends(get_asignacion_aula_service)
):
    return service.create(asignacion)


@router.put("/{id_examen_aula}", response_model=AsignacionAula)
def update_asignacion_aula(
    id_examen_aula: str,
    asignacion_update: AsignacionAulaUpdate,
    service: AsignacionAulaService = Depends(get_asignacion_aula_service)
):
    asignacion = service.update(id_examen_aula, asignacion_update)
    if asignacion is None:
        raise HTTPException(status_code=404, detail="Asignación de aula no encontrada")
    return asignacion


@router.delete("/{id_examen_aula}", response_model=AsignacionAula)
def delete_asignacion_aula(
    id_examen_aula: str,
    service: AsignacionAulaService = Depends(get_asignacion_aula_service)
):
    asignacion = service.delete(id_examen_aula)
    if asignacion is None:
        raise HTTPException(status_code=404, detail="Asignación de aula no encontrada")
    return asignacion