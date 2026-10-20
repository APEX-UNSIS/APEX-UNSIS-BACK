from typing import Optional

from pydantic import BaseModel

from app.schemas.AulaSchema import Aula
from app.schemas.ProfesorSchema import Profesor
from app.schemas.SolicitudExamenSchema import SolicitudExamen


class AsignacionAulaBase(BaseModel):
    id_examen_aula: str
    id_horario: str
    id_aula: str
    id_profesor_aplicador: str


class AsignacionAulaCreate(AsignacionAulaBase):
    pass


class AsignacionAulaUpdate(BaseModel):
    id_aula: Optional[str] = None
    id_profesor_aplicador: Optional[str] = None


class AsignacionAula(AsignacionAulaBase):
    solicitud: Optional[SolicitudExamen] = None
    aula: Optional[Aula] = None
    profesor_aplicador: Optional[Profesor] = None

    class Config:
        from_attributes = True