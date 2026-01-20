from typing import Optional
from pydantic import BaseModel


class UsuarioBase(BaseModel):
    id_usuario: str
    nombre_usuario: str
    id_carrera: Optional[str] = None
    rol: str


class UsuarioCreate(BaseModel):
    id_usuario: str
    nombre_usuario: str
    contraseña: str
    id_carrera: Optional[str] = None
    rol: str
    is_active: bool = True


class UsuarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    contraseña: Optional[str] = None
    id_carrera: Optional[str] = None
    rol: Optional[str] = None
    is_active: Optional[bool] = None


class Usuario(UsuarioBase):
    is_active: bool

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    user: str  # Puede ser id_usuario o nombre_usuario
    password: str


class UsuarioResponse(BaseModel):
    id_usuario: str
    nombre_usuario: str
    id_carrera: Optional[str] = None
    rol: str
    is_active: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    token: str
    user: UsuarioResponse
