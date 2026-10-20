from typing import List, Optional
from sqlalchemy.orm import Session

from app.features.periodos.domain.models import PeriodoAcademico
from app.core.base_repository import BaseRepository
from app.features.periodos.domain.schemas import PeriodoAcademicoCreate, PeriodoAcademicoUpdate


class PeriodoRepository(BaseRepository[PeriodoAcademico, PeriodoAcademicoCreate, PeriodoAcademicoUpdate]):
    def __init__(self, db: Session):
        super().__init__(PeriodoAcademico, db)

    def get_by_id(self, id_periodo: str) -> Optional[PeriodoAcademico]:
        return self.db.query(PeriodoAcademico).filter(PeriodoAcademico.id_periodo == id_periodo).first()