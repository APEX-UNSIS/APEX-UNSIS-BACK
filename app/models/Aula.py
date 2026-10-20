from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Aula(Base):
    __tablename__ = 'aulas'

    id_aula = Column(String(20), primary_key=True)
    nombre_aula = Column(String(50))
    capacidad = Column(Integer)
    is_disable = Column(Boolean, default=False)

    horarios_clase = relationship("HorarioClase", back_populates="aula")
    asignaciones_examen = relationship("AsignacionAula", back_populates="aula")