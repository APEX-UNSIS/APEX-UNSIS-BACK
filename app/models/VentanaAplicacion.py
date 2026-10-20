from sqlalchemy import Column, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base


class VentanaAplicacion(Base):
    __tablename__ = 'ventanas_de_aplicacion_por_periodo'

    id_ventana = Column(String(20), primary_key=True)
    id_periodo = Column(String(20), ForeignKey('periodos_academicos.id_periodo'))
    id_evaluacion = Column(String(20), ForeignKey('tipos_de_evaluacion.id_evaluacion'))
    fecha_inicio_examenes = Column(Date)
    fecha_fin_examenes = Column(Date)

    periodo = relationship("PeriodoAcademico", back_populates="ventanas_aplicacion")
    evaluacion = relationship("TipoEvaluacion", back_populates="ventanas_aplicacion")