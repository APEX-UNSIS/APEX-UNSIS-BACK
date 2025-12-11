from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.PeriodoRepository import PeriodoRepository
from app.schemas.PeriodoAcademicoSchema import PeriodoAcademico, PeriodoAcademicoCreate, PeriodoAcademicoUpdate
from app.services.PeriodoService import PeriodoService

router = APIRouter(prefix="/periodos", tags=["periodos"])


def get_periodo_service(db: Session = Depends(get_db)) -> PeriodoService:
    repository = PeriodoRepository(db)
    return PeriodoService(repository)


@router.get("/", response_model=List[PeriodoAcademico])
def read_periodos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: PeriodoService = Depends(get_periodo_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{id_periodo}", response_model=PeriodoAcademico)
def read_periodo(
    id_periodo: str,
    service: PeriodoService = Depends(get_periodo_service)
):
    periodo = service.get(id_periodo)
    if periodo is None:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    return periodo


@router.post("/", response_model=PeriodoAcademico)
def create_periodo(
    periodo: PeriodoAcademicoCreate,
    service: PeriodoService = Depends(get_periodo_service)
):
    return service.create(periodo)


@router.put("/{id_periodo}", response_model=PeriodoAcademico)
def update_periodo(
    id_periodo: str,
    periodo_update: PeriodoAcademicoUpdate,
    service: PeriodoService = Depends(get_periodo_service)
):
    periodo = service.update(id_periodo, periodo_update)
    if periodo is None:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    return periodo


@router.delete("/{id_periodo}", response_model=PeriodoAcademico)
def delete_periodo(
    id_periodo: str,
    service: PeriodoService = Depends(get_periodo_service)
):
    periodo = service.delete(id_periodo)
    if periodo is None:
        raise HTTPException(status_code=404, detail="Periodo no encontrado")
    return periodo