from typing import List, Optional

from app.models.HorarioClase import HorarioClase
from app.repositories.HorarioRepository import HorarioRepository
from app.schemas.HorarioClaseSchema import HorarioClaseCreate, HorarioClaseUpdate
from app.services.base_service import BaseService


class HorarioService(BaseService[HorarioClase, HorarioClaseCreate, HorarioClaseUpdate]):
    def __init__(self, repository: HorarioRepository):
        super().__init__(repository)
        self.repository = repository

    def get_with_relations(self, id_horario: str) -> Optional[HorarioClase]:
        return self.repository.get_with_relations(id_horario)

    def get_by_profesor(self, id_profesor: str, skip: int = 0, limit: int = 100) -> List[HorarioClase]:
        return self.repository.get_by_profesor(id_profesor, skip, limit)

    def get_by_grupo(self, id_grupo: str, skip: int = 0, limit: int = 100) -> List[HorarioClase]:
        return self.repository.get_by_grupo(id_grupo, skip, limit)

    def get_by_carrera(self, id_carrera: str, skip: int = 0, limit: int = 100) -> List[HorarioClase]:
        return self.repository.get_by_carrera(id_carrera, skip, limit)