from app.features.evaluaciones.domain.models import TipoEvaluacion
from app.features.evaluaciones.infrastructure.repository import EvaluacionRepository
from app.features.evaluaciones.domain.schemas import TipoEvaluacionCreate, TipoEvaluacionUpdate
from app.core.base_service import BaseService


class EvaluacionService(BaseService[TipoEvaluacion, TipoEvaluacionCreate, TipoEvaluacionUpdate]):
    def __init__(self, repository: EvaluacionRepository):
        super().__init__(repository)
        self.repository = repository