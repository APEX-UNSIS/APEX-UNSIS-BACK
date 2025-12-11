from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database import Base


class TipoEvaluacion(Base):
    __tablename__ = 'tipos_de_evaluacion'

    id_evaluacion = Column(String(20), primary_key=True)
    nombre_evaluacion = Column(String(30))

    ventanas_aplicacion = relationship("VentanaAplicacion", back_populates="evaluacion")
    solicitudes_examen = relationship("SolicitudExamen", back_populates="evaluacion")