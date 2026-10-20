from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
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


class SalaComputo(Base):
    """
    Registro de aulas que son salas de cómputo (para exámenes en plataforma).
    No son materias; solo indican qué aulas usar cuando tipo_examen = 'plataforma'.
    """
    __tablename__ = 'salas_de_computo'

    id_aula = Column(String(20), ForeignKey('aulas.id_aula'), primary_key=True)

    aula = relationship("Aula", backref="es_sala_computo")
