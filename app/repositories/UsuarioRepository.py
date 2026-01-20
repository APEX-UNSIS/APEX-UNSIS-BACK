from typing import Optional
from sqlalchemy.orm import Session

from app.models.Usuario import Usuario
from app.repositories.base_repository import BaseRepository
from app.schemas.UsuarioSchema import UsuarioCreate, UsuarioUpdate


class UsuarioRepository(BaseRepository[Usuario, UsuarioCreate, UsuarioUpdate]):
    def __init__(self, db: Session):
        super().__init__(Usuario, db)

    def get_by_id_usuario(self, id_usuario: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    def get_by_nombre_usuario(self, nombre_usuario: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()

    def get_by_username_or_id(self, username: str) -> Optional[Usuario]:
        """
        Busca un usuario por id_usuario o nombre_usuario
        """
        usuario = self.db.query(Usuario).filter(
            (Usuario.id_usuario == username) | (Usuario.nombre_usuario == username)
        ).first()
        return usuario

    def get_by_rol(self, rol: str, skip: int = 0, limit: int = 100):
        return self.db.query(Usuario).filter(
            Usuario.rol == rol,
            Usuario.is_active == True
        ).offset(skip).limit(limit).all()
