from app.models.TipoEvaluacion import TipoEvaluacion
from app.repositories.EvaluacionRepository import EvaluacionRepository
from app.schemas.TipoEvaluacionSchema import TipoEvaluacionCreate, TipoEvaluacionUpdate
from app.services.base_service import BaseService


class EvaluacionService(BaseService[TipoEvaluacion, TipoEvaluacionCreate, TipoEvaluacionUpdate]):
    def __init__(self, repository: EvaluacionRepository):
        super().__init__(repository)
        self.repository = repository