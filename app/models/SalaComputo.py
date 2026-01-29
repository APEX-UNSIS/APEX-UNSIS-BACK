from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class SalaComputo(Base):
    """
    Registro de aulas que son salas de cómputo (para exámenes en plataforma).
    No son materias; solo indican qué aulas usar cuando tipo_examen = 'plataforma'.
    """
    __tablename__ = 'salas_de_computo'

    id_aula = Column(String(20), ForeignKey('aulas.id_aula'), primary_key=True)

    aula = relationship("Aula", backref="es_sala_computo")
