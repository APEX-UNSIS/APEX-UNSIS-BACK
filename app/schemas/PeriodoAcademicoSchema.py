from typing import Optional

from pydantic import BaseModel


class PeriodoAcademicoBase(BaseModel):
    id_periodo: str
    nombre_periodo: str


class PeriodoAcademicoCreate(PeriodoAcademicoBase):
    pass


class PeriodoAcademicoUpdate(BaseModel):
    nombre_periodo: Optional[str] = None


class PeriodoAcademico(PeriodoAcademicoBase):
    class Config:
        from_attributes = True