from typing import List, Optional
from sqlalchemy.orm import Session

from app.features.evaluaciones.domain.models import TipoEvaluacion
from app.core.base_repository import BaseRepository
from app.features.evaluaciones.domain.schemas import TipoEvaluacionCreate, TipoEvaluacionUpdate


class EvaluacionRepository(BaseRepository[TipoEvaluacion, TipoEvaluacionCreate, TipoEvaluacionUpdate]):
    def __init__(self, db: Session):
        super().__init__(TipoEvaluacion, db)

    def get_by_id(self, id_evaluacion: str) -> Optional[TipoEvaluacion]:
        return self.db.query(TipoEvaluacion).filter(TipoEvaluacion.id_evaluacion == id_evaluacion).first()