from datetime import date, time
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.features.evaluaciones.domain.schemas import TipoEvaluacion
from app.features.materias.domain.schemas import Materia
from app.features.periodos.domain.schemas import PeriodoAcademico


class EstadoSolicitud(int, Enum):
    PENDIENTE = 0
    APROBADO = 1
    RECHAZADO = 2


class SolicitudExamenBase(BaseModel):
    id_horario: str
    id_periodo: str
    id_evaluacion: str
    id_materia: str
    fecha_examen: date
    hora_inicio: time
    hora_fin: time
    estado: EstadoSolicitud = EstadoSolicitud.PENDIENTE
    motivo_rechazo: Optional[str] = None
    is_manualmente_editado: bool = False


class SolicitudExamenCreate(SolicitudExamenBase):
    pass


class SolicitudExamenUpdate(BaseModel):
    estado: Optional[EstadoSolicitud] = None
    motivo_rechazo: Optional[str] = None
    is_manualmente_editado: Optional[bool] = None


class SolicitudExamen(SolicitudExamenBase):
    periodo: Optional[PeriodoAcademico] = None
    evaluacion: Optional[TipoEvaluacion] = None
    materia: Optional[Materia] = None

    class Config:
        from_attributes = True
