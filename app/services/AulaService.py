from typing import List, Optional

from app.models.Aula import Aula
from app.repositories.AulaRepository import AulaRepository
from app.schemas.AulaSchema import AulaCreate, AulaUpdate
from app.services.base_service import BaseService


class AulaService(BaseService[Aula, AulaCreate, AulaUpdate]):
    def __init__(self, repository: AulaRepository):
        super().__init__(repository)
        self.repository = repository

    def get_disponibles(self, capacidad_minima: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Aula]:
        return self.repository.get_disponibles(capacidad_minima, skip, limit)