from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.EvaluacionRepository import EvaluacionRepository
from app.schemas.TipoEvaluacionSchema import TipoEvaluacion, TipoEvaluacionCreate, TipoEvaluacionUpdate
from app.services.EvaluacionService import EvaluacionService

router = APIRouter(prefix="/evaluaciones", tags=["evaluaciones"])


def get_evaluacion_service(db: Session = Depends(get_db)) -> EvaluacionService:
    repository = EvaluacionRepository(db)
    return EvaluacionService(repository)


@router.get("/", response_model=List[TipoEvaluacion])
def read_evaluaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    service: EvaluacionService = Depends(get_evaluacion_service)
):
    return service.get_all(skip=skip, limit=limit)


@router.get("/{id_evaluacion}", response_model=TipoEvaluacion)
def read_evaluacion(
    id_evaluacion: str,
    service: EvaluacionService = Depends(get_evaluacion_service)
):
    evaluacion = service.get(id_evaluacion)
    if evaluacion is None:
        raise HTTPException(status_code=404, detail="Tipo de evaluación no encontrado")
    return evaluacion


@router.post("/", response_model=TipoEvaluacion)
def create_evaluacion(
    evaluacion: TipoEvaluacionCreate,
    service: EvaluacionService = Depends(get_evaluacion_service)
):
    return service.create(evaluacion)


@router.put("/{id_evaluacion}", response_model=TipoEvaluacion)
def update_evaluacion(
    id_evaluacion: str,
    evaluacion_update: TipoEvaluacionUpdate,
    service: EvaluacionService = Depends(get_evaluacion_service)
):
    evaluacion = service.update(id_evaluacion, evaluacion_update)
    if evaluacion is None:
        raise HTTPException(status_code=404, detail="Tipo de evaluación no encontrado")
    return evaluacion


@router.delete("/{id_evaluacion}", response_model=TipoEvaluacion)
def delete_evaluacion(
    id_evaluacion: str,
    service: EvaluacionService = Depends(get_evaluacion_service)
):
    evaluacion = service.delete(id_evaluacion)
    if evaluacion is None:
        raise HTTPException(status_code=404, detail="Tipo de evaluación no encontrado")
    return evaluacion