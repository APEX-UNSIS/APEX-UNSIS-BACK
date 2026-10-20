from typing import List, Optional

from app.models.GrupoEscolar import GrupoEscolar
from app.repositories.GrupoRepository import GrupoRepository
from app.schemas.GrupoEscolarSchema import GrupoEscolarCreate, GrupoEscolarUpdate
from app.services.base_service import BaseService


class GrupoService(BaseService[GrupoEscolar, GrupoEscolarCreate, GrupoEscolarUpdate]):
    def __init__(self, repository: GrupoRepository):
        super().__init__(repository)
        self.repository = repository

    def get_with_carrera(self, id_grupo: str) -> Optional[GrupoEscolar]:
        return self.repository.get_with_carrera(id_grupo)

    def get_by_carrera(self, id_carrera: str, skip: int = 0, limit: int = 100) -> List[GrupoEscolar]:
        return self.repository.get_by_carrera(id_carrera, skip, limit)