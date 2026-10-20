from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class GrupoEscolar(Base):
    __tablename__ = 'grupos_escolares'

    id_grupo = Column(String(20), primary_key=True)
    nombre_grupo = Column(String(20))
    numero_alumnos = Column(Integer)
    id_carrera = Column(String(20), ForeignKey('carreras.id_carrera'))

    carrera = relationship("Carrera", back_populates="grupos")
    horarios_clase = relationship("HorarioClase", back_populates="grupo")
    grupos_examen = relationship("GrupoExamen", back_populates="grupo")