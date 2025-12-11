from typing import List

from app.models.Profesor import Profesor
from app.repositories.ProfesorRepository import ProfesorRepository
from app.schemas.ProfesorSchema import ProfesorCreate, ProfesorUpdate
from app.services.base_service import BaseService


class ProfesorService(BaseService[Profesor, ProfesorCreate, ProfesorUpdate]):
    def __init__(self, repository: ProfesorRepository):
        super().__init__(repository)
        self.repository = repository

    def get_activos(self, skip: int = 0, limit: int = 100) -> List[Profesor]:
        return self.repository.get_activos(skip, limit)