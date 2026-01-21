from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    id_usuario: str
    nombre_usuario: str
    email: Optional[str] = None
    id_carrera: Optional[str] = None
    rol: str


class UsuarioCreate(BaseModel):
    id_usuario: str
    nombre_usuario: str
    email: Optional[str] = None
    contraseña: str
    id_carrera: Optional[str] = None
    rol: str
    is_active: bool = True


class UsuarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    email: Optional[str] = None
    contraseña: Optional[str] = None
    id_carrera: Optional[str] = None
    rol: Optional[str] = None
    is_active: Optional[bool] = None


class Usuario(UsuarioBase):
    is_active: bool
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    user: str  # Puede ser id_usuario o nombre_usuario
    password: str


class UsuarioResponse(BaseModel):
    id_usuario: str
    nombre_usuario: str
    email: Optional[str] = None
    id_carrera: Optional[str] = None
    rol: str
    is_active: bool
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    token: str
    user: UsuarioResponse

