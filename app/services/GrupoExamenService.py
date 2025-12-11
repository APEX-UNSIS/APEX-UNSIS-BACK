from typing import List

from app.models.GrupoExamen import GrupoExamen
from app.repositories.GrupoExamenRepository import GrupoExamenRepository
from app.schemas.GrupoExamenSchema import GrupoExamenCreate, GrupoExamenUpdate
from app.services.base_service import BaseService


class GrupoExamenService(BaseService[GrupoExamen, GrupoExamenCreate, GrupoExamenUpdate]):
    def __init__(self, repository: GrupoExamenRepository):
        super().__init__(repository)
        self.repository = repository

    def get_by_solicitud(self, id_horario: str) -> List[GrupoExamen]:
        return self.repository.get_by_solicitud(id_horario)

    def get_by_grupo(self, id_grupo: str) -> List[GrupoExamen]:
        return self.repository.get_by_grupo(id_grupo)