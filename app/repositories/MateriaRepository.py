from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.Materia import Materia
from app.repositories.base_repository import BaseRepository
from app.schemas.MateriaSchema import MateriaCreate, MateriaUpdate


class MateriaRepository(BaseRepository[Materia, MateriaCreate, MateriaUpdate]):
    def __init__(self, db: Session):
        super().__init__(Materia, db)

    def get_by_id(self, id_materia: str) -> Optional[Materia]:
        return self.db.query(Materia).filter(Materia.id_materia == id_materia).first()

    def get_by_nombre(self, nombre: str) -> Optional[Materia]:
        return self.db.query(Materia).filter(Materia.nombre_materia == nombre).first()