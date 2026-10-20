from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.TipoEvaluacion import TipoEvaluacion
from app.repositories.base_repository import BaseRepository
from app.schemas.TipoEvaluacionSchema import TipoEvaluacionCreate, TipoEvaluacionUpdate


class EvaluacionRepository(BaseRepository[TipoEvaluacion, TipoEvaluacionCreate, TipoEvaluacionUpdate]):
    def __init__(self, db: Session):
        super().__init__(TipoEvaluacion, db)

    def get_by_id(self, id_evaluacion: str) -> Optional[TipoEvaluacion]:
        return self.db.query(TipoEvaluacion).filter(TipoEvaluacion.id_evaluacion == id_evaluacion).first()