from typing import Optional

from pydantic import BaseModel

from app.features.profesores.domain.schemas import Profesor
from app.features.solicitudes.domain.schemas import SolicitudExamen


class AsignacionSinodalBase(BaseModel):
    id_examen_sinodal: str
    id_horario: str
    id_profesor: str


class AsignacionSinodalCreate(AsignacionSinodalBase):
    pass


class AsignacionSinodalUpdate(BaseModel):
    id_profesor: Optional[str] = None


class AsignacionSinodal(AsignacionSinodalBase):
    solicitud: Optional[SolicitudExamen] = None
    profesor: Optional[Profesor] = None

    class Config:
        from_attributes = True