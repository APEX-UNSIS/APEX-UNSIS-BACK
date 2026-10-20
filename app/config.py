from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configuración de la aplicación cargada desde variables de entorno
    """
    # Configuración de Base de Datos
    db_host: str
    db_port: int = 5432
    db_user: str
    db_password: str
    db_name: str
    
    # Configuración de la Aplicación
    app_env: str = "development"
    secret_key: str = "tu-clave-secreta-muy-segura-cambiar-en-produccion"
    # CORS: orígenes permitidos separados por coma (ej. "https://midominio.com,http://192.168.1.10"). Vacío = usar defaults.
    cors_origins: str = ""
    # Clave para resetear contraseña de admin (solo para uso puntual). Si está vacía, el endpoint no hace nada.
    reset_admin_key: str = ""
    
    @property
    def database_url(self) -> str:
        """
        Construye la URL de conexión a PostgreSQL
        """
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Retorna una instancia cacheada de Settings
    """
    return Settings()
