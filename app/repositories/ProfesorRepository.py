from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.Profesor import Profesor
from app.repositories.base_repository import BaseRepository
from app.schemas.ProfesorSchema import ProfesorCreate, ProfesorUpdate


class ProfesorRepository(BaseRepository[Profesor, ProfesorCreate, ProfesorUpdate]):
    def __init__(self, db: Session):
        super().__init__(Profesor, db)

    def get_by_id(self, id_profesor: str) -> Optional[Profesor]:
        return self.db.query(Profesor).filter(Profesor.id_profesor == id_profesor).first()

    def get_activos(self, skip: int = 0, limit: int = 100) -> List[Profesor]:
        return self.db.query(Profesor).filter(
            Profesor.is_disable == False
        ).offset(skip).limit(limit).all()