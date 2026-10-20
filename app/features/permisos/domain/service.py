from typing import List, Optional

from app.features.permisos.domain.models import PermisoSinodal
from app.features.permisos.infrastructure.repository import PermisoRepository
from app.features.permisos.domain.schemas import PermisoSinodalCreate, PermisoSinodalUpdate
from app.core.base_service import BaseService


class PermisoService(BaseService[PermisoSinodal, PermisoSinodalCreate, PermisoSinodalUpdate]):
    def __init__(self, repository: PermisoRepository):
        super().__init__(repository)
        self.repository = repository

    def get_by_profesor_materia(self, id_profesor: str, id_materia: str) -> Optional[PermisoSinodal]:
        return self.repository.get_by_profesor_materia(id_profesor, id_materia)

    def get_by_profesor(self, id_profesor: str) -> List[PermisoSinodal]:
        return self.repository.get_by_profesor(id_profesor)

    def get_by_materia(self, id_materia: str) -> List[PermisoSinodal]:
        return self.repository.get_by_materia(id_materia)