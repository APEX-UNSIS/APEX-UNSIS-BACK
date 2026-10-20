from app.models.PeriodoAcademico import PeriodoAcademico
from app.repositories.PeriodoRepository import PeriodoRepository
from app.schemas.PeriodoAcademicoSchema import PeriodoAcademicoCreate, PeriodoAcademicoUpdate
from app.services.base_service import BaseService


class PeriodoService(BaseService[PeriodoAcademico, PeriodoAcademicoCreate, PeriodoAcademicoUpdate]):
    def __init__(self, repository: PeriodoRepository):
        super().__init__(repository)
        self.repository = repository