from typing import Optional

from pydantic import BaseModel

from app.schemas.GrupoEscolarSchema import GrupoEscolar
from app.schemas.SolicitudExamenSchema import SolicitudExamen


class GrupoExamenBase(BaseModel):
    id_examen_grupo: str
    id_horario: str
    id_grupo: str


class GrupoExamenCreate(GrupoExamenBase):
    pass


class GrupoExamenUpdate(BaseModel):
    id_grupo: Optional[str] = None


class GrupoExamen(GrupoExamenBase):
    solicitud: Optional[SolicitudExamen] = None
    grupo: Optional[GrupoEscolar] = None

    class Config:
        orm_mode = True