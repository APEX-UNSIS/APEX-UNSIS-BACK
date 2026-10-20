from typing import List, Optional

from app.features.grupos.domain.models import GrupoEscolar
from app.features.grupos.infrastructure.repository import GrupoRepository
from app.features.grupos.domain.schemas import GrupoEscolarCreate, GrupoEscolarUpdate
from app.core.base_service import BaseService


class GrupoService(BaseService[GrupoEscolar, GrupoEscolarCreate, GrupoEscolarUpdate]):
    def __init__(self, repository: GrupoRepository):
        super().__init__(repository)
        self.repository = repository

    def get_with_carrera(self, id_grupo: str) -> Optional[GrupoEscolar]:
        return self.repository.get_with_carrera(id_grupo)

    def get_by_carrera(self, id_carrera: str, skip: int = 0, limit: int = 100) -> List[GrupoEscolar]:
        return self.repository.get_by_carrera(id_carrera, skip, limit)