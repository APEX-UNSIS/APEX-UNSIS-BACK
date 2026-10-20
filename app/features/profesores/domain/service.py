from typing import List

from app.features.profesores.domain.models import Profesor
from app.features.profesores.infrastructure.repository import ProfesorRepository
from app.features.profesores.domain.schemas import ProfesorCreate, ProfesorUpdate
from app.core.base_service import BaseService


class ProfesorService(BaseService[Profesor, ProfesorCreate, ProfesorUpdate]):
    def __init__(self, repository: ProfesorRepository):
        super().__init__(repository)
        self.repository = repository

    def get_activos(self, skip: int = 0, limit: int = 100) -> List[Profesor]:
        return self.repository.get_activos(skip, limit)

    def get_by_carrera(self, id_carrera: str, skip: int = 0, limit: int = 100) -> List[Profesor]:
        return self.repository.get_by_carrera(id_carrera, skip, limit)

    def get_sinodales_by_carrera(self, id_carrera: str, skip: int = 0, limit: int = 100) -> List[Profesor]:
        return self.repository.get_sinodales_by_carrera(id_carrera, skip, limit)