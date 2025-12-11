from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.Aula import Aula
from app.repositories.base_repository import BaseRepository
from app.schemas.AulaSchema import AulaCreate, AulaUpdate


class AulaRepository(BaseRepository[Aula, AulaCreate, AulaUpdate]):
    def __init__(self, db: Session):
        super().__init__(Aula, db)

    def get_by_id(self, id_aula: str) -> Optional[Aula]:
        return self.db.query(Aula).filter(Aula.id_aula == id_aula).first()

    def get_disponibles(self, capacidad_minima: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Aula]:
        query = self.db.query(Aula).filter(Aula.is_disable == False)

        if capacidad_minima:
            query = query.filter(Aula.capacidad >= capacidad_minima)

        return query.offset(skip).limit(limit).all()