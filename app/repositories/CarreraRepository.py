from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.Carrera import Carrera
from app.repositories.base_repository import BaseRepository
from app.schemas.CarreraSchema import CarreraCreate, CarreraUpdate


class CarreraRepository(BaseRepository[Carrera, CarreraCreate, CarreraUpdate]):
    def __init__(self, db: Session):
        super().__init__(Carrera, db)

    def get_by_id(self, id_carrera: str) -> Optional[Carrera]:
        return self.db.query(Carrera).filter(Carrera.id_carrera == id_carrera).first()

    def get_by_nombre(self, nombre: str) -> Optional[Carrera]:
        return self.db.query(Carrera).filter(Carrera.nombre_carrera == nombre).first()

    def search_by_nombre(self, nombre: str, skip: int = 0, limit: int = 100) -> List[Carrera]:
        return self.db.query(Carrera).filter(
            Carrera.nombre_carrera.ilike(f"%{nombre}%")
        ).offset(skip).limit(limit).all()