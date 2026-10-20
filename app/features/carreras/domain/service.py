from typing import List, Optional

from app.features.carreras.domain.models import Carrera
from app.features.carreras.infrastructure.repository import CarreraRepository
from app.features.carreras.domain.schemas import CarreraCreate, CarreraUpdate
from app.core.base_service import BaseService


class CarreraService(BaseService[Carrera, CarreraCreate, CarreraUpdate]):
    def __init__(self, repository: CarreraRepository):
        super().__init__(repository)
        self.repository = repository

    def get_by_nombre(self, nombre: str) -> Optional[Carrera]:
        return self.repository.get_by_nombre(nombre)

    def search_by_nombre(self, nombre: str, skip: int = 0, limit: int = 100) -> List[Carrera]:
        return self.repository.search_by_nombre(nombre, skip, limit)