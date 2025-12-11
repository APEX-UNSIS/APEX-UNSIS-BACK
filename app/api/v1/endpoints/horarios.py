from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.HorarioRepository import HorarioRepository
from app.schemas.HorarioClaseSchema import HorarioClase, HorarioClaseCreate, HorarioClaseUpdate
from app.services.HorarioService import HorarioService

router = APIRouter(prefix="/horarios", tags=["horarios"])


def get_horario_service(db: Session = Depends(get_db)) -> HorarioService:
    repository = HorarioRepository(db)
    return HorarioService(repository)


@router.get("/", response_model=List[HorarioClase])
def read_horarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: HorarioService = Depends(get_horario_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{id_horario}", response_model=HorarioClase)
def read_horario(
    id_horario: str,
    service: HorarioService = Depends(get_horario_service)
):
    horario = service.get(id_horario)
    if horario is None:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario


@router.get("/{id_horario}/completo", response_model=HorarioClase)
def read_horario_completo(
    id_horario: str,
    service: HorarioService = Depends(get_horario_service)
):
    horario = service.get_with_relations(id_horario)
    if horario is None:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario


@router.get("/profesor/{id_profesor}", response_model=List[HorarioClase])
def read_horarios_por_profesor(
    id_profesor: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: HorarioService = Depends(get_horario_service)
):
    return service.get_by_profesor(id_profesor, skip=skip, limit=limit)


@router.get("/grupo/{id_grupo}", response_model=List[HorarioClase])
def read_horarios_por_grupo(
    id_grupo: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: HorarioService = Depends(get_horario_service)
):
    return service.get_by_grupo(id_grupo, skip=skip, limit=limit)


@router.post("/", response_model=HorarioClase)
def create_horario(
    horario: HorarioClaseCreate,
    service: HorarioService = Depends(get_horario_service)
):
    return service.create(horario)


@router.put("/{id_horario}", response_model=HorarioClase)
def update_horario(
    id_horario: str,
    horario_update: HorarioClaseUpdate,
    service: HorarioService = Depends(get_horario_service)
):
    horario = service.update(id_horario, horario_update)
    if horario is None:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario


@router.delete("/{id_horario}", response_model=HorarioClase)
def delete_horario(
    id_horario: str,
    service: HorarioService = Depends(get_horario_service)
):
    horario = service.delete(id_horario)
    if horario is None:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario