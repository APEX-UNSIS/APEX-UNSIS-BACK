from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class GrupoExamen(Base):
    __tablename__ = 'grupos_por_solicitud_de_examen'

    id_examen_grupo = Column(String(20), primary_key=True)
    id_horario = Column(String(20), ForeignKey('solicitudes_de_examen.id_horario'))
    id_grupo = Column(String(20), ForeignKey('grupos_escolares.id_grupo'))

    solicitud = relationship("SolicitudExamen", back_populates="grupos_examen")
    grupo = relationship("GrupoEscolar", back_populates="grupos_examen")