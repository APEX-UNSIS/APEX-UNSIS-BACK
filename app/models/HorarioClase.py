from sqlalchemy import Column, String, ForeignKey, Integer, Time
from sqlalchemy.orm import relationship

from app.database import Base


class HorarioClase(Base):
    __tablename__ = 'horarios_regulares_de_clase'

    id_horario_clase = Column(String(20), primary_key=True)
    id_periodo = Column(String(20), ForeignKey('periodos_academicos.id_periodo'))
    id_materia = Column(String(20), ForeignKey('materias.id_materia'))
    id_grupo = Column(String(20), ForeignKey('grupos_escolares.id_grupo'))
    id_profesor = Column(String(20), ForeignKey('profesores.id_profesor'))
    id_aula = Column(String(20), ForeignKey('aulas.id_aula'))
    dia_semana = Column(Integer)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)

    periodo = relationship("PeriodoAcademico", back_populates="horarios_clase")
    materia = relationship("Materia", back_populates="horarios_clase")
    grupo = relationship("GrupoEscolar", back_populates="horarios_clase")
    profesor = relationship("Profesor", back_populates="horarios_clase")
    aula = relationship("Aula", back_populates="horarios_clase")