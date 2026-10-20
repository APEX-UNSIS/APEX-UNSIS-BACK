from typing import Optional

from pydantic import BaseModel


class TipoEvaluacionBase(BaseModel):
    id_evaluacion: str
    nombre_evaluacion: str


class TipoEvaluacionCreate(TipoEvaluacionBase):
    pass


class TipoEvaluacionUpdate(BaseModel):
    nombre_evaluacion: Optional[str] = None


class TipoEvaluacion(TipoEvaluacionBase):
    class Config:
        from_attributes = True