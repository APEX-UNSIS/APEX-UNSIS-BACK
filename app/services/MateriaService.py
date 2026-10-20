from typing import Optional, List

from app.models.Materia import Materia
from app.repositories.MateriaRepository import MateriaRepository
from app.schemas.MateriaSchema import MateriaCreate, MateriaUpdate
from app.services.base_service import BaseService


class MateriaService(BaseService[Materia, MateriaCreate, MateriaUpdate]):
    def __init__(self, repository: MateriaRepository):
        super().__init__(repository)
        self.repository = repository

    def get_by_nombre(self, nombre: str) -> Optional[Materia]:
        return self.repository.get_by_nombre(nombre)

    def get_by_carrera(self, id_carrera: str, skip: int = 0, limit: int = 100, id_periodo: Optional[str] = None, id_grupo: Optional[str] = None) -> List[Materia]:
        return self.repository.get_by_carrera(id_carrera, skip, limit, id_periodo, id_grupo)