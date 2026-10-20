"""
Paquete de features (arquitectura hexagonal por dominio).

Importar aquí todos los modelos garantiza que SQLAlchemy registre cada tabla
y sus relaciones (resueltas por nombre) antes de `Base.metadata.create_all()`
en el arranque de la aplicación.
"""
from app.features.asignaciones_aulas.domain import models as _asignaciones_aulas_models  # noqa: F401
from app.features.asignaciones_sinodales.domain import models as _asignaciones_sinodales_models  # noqa: F401
from app.features.aulas.domain import models as _aulas_models  # noqa: F401
from app.features.carreras.domain import models as _carreras_models  # noqa: F401
from app.features.evaluaciones.domain import models as _evaluaciones_models  # noqa: F401
from app.features.grupos.domain import models as _grupos_models  # noqa: F401
from app.features.grupos_examen.domain import models as _grupos_examen_models  # noqa: F401
from app.features.horarios.domain import models as _horarios_models  # noqa: F401
from app.features.materias.domain import models as _materias_models  # noqa: F401
from app.features.periodos.domain import models as _periodos_models  # noqa: F401
from app.features.permisos.domain import models as _permisos_models  # noqa: F401
from app.features.profesores.domain import models as _profesores_models  # noqa: F401
from app.features.solicitudes.domain import models as _solicitudes_models  # noqa: F401
from app.features.usuarios.domain import models as _usuarios_models  # noqa: F401
from app.features.ventanas.domain import models as _ventanas_models  # noqa: F401
