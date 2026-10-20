from typing import Optional

from pydantic import BaseModel

from app.schemas.ProfesorSchema import Profesor
from app.schemas.SolicitudExamenSchema import SolicitudExamen


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