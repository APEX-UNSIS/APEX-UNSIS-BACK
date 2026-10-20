from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.PeriodoAcademico import PeriodoAcademico
from app.repositories.base_repository import BaseRepository
from app.schemas.PeriodoAcademicoSchema import PeriodoAcademicoCreate, PeriodoAcademicoUpdate


class PeriodoRepository(BaseRepository[PeriodoAcademico, PeriodoAcademicoCreate, PeriodoAcademicoUpdate]):
    def __init__(self, db: Session):
        super().__init__(PeriodoAcademico, db)

    def get_by_id(self, id_periodo: str) -> Optional[PeriodoAcademico]:
        return self.db.query(PeriodoAcademico).filter(PeriodoAcademico.id_periodo == id_periodo).first()