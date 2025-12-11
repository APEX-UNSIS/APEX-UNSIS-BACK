from datetime import date, time
from typing import Optional

from pydantic import BaseModel

from app.schemas.EstadoSolicitudSchema import EstadoSolicitud
from app.schemas.MateriaSchema import Materia
from app.schemas.PeriodoAcademicoSchema import PeriodoAcademico
from app.schemas.TipoEvaluacionSchema import TipoEvaluacion


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
        orm_mode = True