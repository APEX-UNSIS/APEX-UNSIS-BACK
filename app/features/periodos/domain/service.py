from app.features.periodos.domain.models import PeriodoAcademico
from app.features.periodos.infrastructure.repository import PeriodoRepository
from app.features.periodos.domain.schemas import PeriodoAcademicoCreate, PeriodoAcademicoUpdate
from app.core.base_service import BaseService


class PeriodoService(BaseService[PeriodoAcademico, PeriodoAcademicoCreate, PeriodoAcademicoUpdate]):
    def __init__(self, repository: PeriodoRepository):
        super().__init__(repository)
        self.repository = repository