from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.v1.endpoints import api_router
from app.database import get_db, init_db
from app.config import get_settings
# Importar modelos para que se registren en SQLAlchemy al inicializar la base de datos
from app.models import Usuario, Carrera  # noqa: F401

# Obtener configuración
settings = get_settings()

app = FastAPI(
    title="Mi App FastAPI",
    description="Aplicación web con FastAPI y PostgreSQL",
    version="1.0.0"
)

# Configurar CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta al iniciar la aplicación
    Inicializa las tablas de la base de datos
    """
    init_db()
    print(f"Aplicación iniciada en modo: {settings.app_env}")
    print(f"Conectado a la base de datos: {settings.db_name}")


@app.get("/")
def read_root():
    return {"mensaje": "¡Hola Mundo desde FastAPI!"}


@app.get("/carreras")
def get_carreras(db: Session = Depends(get_db)):
    """
    Obtener todas las carreras de la base de datos
    """
    try:
        result = db.execute(text("SELECT * FROM carreras"))
        carreras = []
        for row in result:
            carreras.append(dict(row._mapping))
        return {
            "status": "success",
            "data": carreras,
            "total": len(carreras)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al consultar carreras: {str(e)}"
        }

app.include_router(api_router, prefix="/api/v1")