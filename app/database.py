from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

# Obtener configuración
settings = get_settings()

# Engine de SQLAlchemy
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
    echo=True if settings.app_env == "development" else False  # Log de SQL en desarrollo
)

# SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Generador de dependencia para obtener una sesión de base de datos
    Uso en FastAPI: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa la base de datos creando todas las tablas
    """
    Base.metadata.create_all(bind=engine)
