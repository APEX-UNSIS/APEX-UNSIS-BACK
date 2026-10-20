from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database import Base


class Carrera(Base):
    __tablename__ = 'carreras'

    id_carrera = Column(String(20), primary_key=True)
    nombre_carrera = Column(String(100))

    grupos = relationship("GrupoEscolar", back_populates="carrera")