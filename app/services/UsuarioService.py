from typing import Optional
import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.Usuario import Usuario
from app.repositories.UsuarioRepository import UsuarioRepository
from app.schemas.UsuarioSchema import UsuarioCreate, UsuarioUpdate


class UsuarioService:
    def __init__(self, repository: UsuarioRepository):
        self.repository = repository

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña en texto plano coincide con el hash"""
        try:
            if not hashed_password or not plain_password:
                print(f"[DEBUG] verify_password: hash o password vacío")
                return False
            
            # Limpiar el hash (eliminar espacios y caracteres extra)
            hashed_password = hashed_password.strip()
            
            # Verificar que el hash tenga el formato correcto de bcrypt
            if not hashed_password.startswith('$2b$') and not hashed_password.startswith('$2a$') and not hashed_password.startswith('$2y$'):
                print(f"[DEBUG] verify_password: Hash no tiene formato bcrypt válido. Empieza con: {hashed_password[:10]}")
                return False
            
            # Convertir a bytes si es necesario
            if isinstance(hashed_password, str):
                hashed_password_bytes = hashed_password.encode('utf-8')
            else:
                hashed_password_bytes = hashed_password
            
            if isinstance(plain_password, str):
                plain_password_bytes = plain_password.encode('utf-8')
            else:
                plain_password_bytes = plain_password
            
            # Verificar con bcrypt directamente
            result = bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
            print(f"[DEBUG] verify_password: Resultado de bcrypt.checkpw: {result}")
            if not result:
                # Intentar verificar si el hash tiene algún problema de codificación
                print(f"[DEBUG] verify_password: Hash completo: {hashed_password}")
                print(f"[DEBUG] verify_password: Password recibida: '{plain_password}' (bytes: {plain_password_bytes})")
            return result
        except Exception as e:
            print(f"[DEBUG] Error verificando contraseña: {str(e)}")
            print(f"[DEBUG] Hash recibido (longitud: {len(hashed_password) if hashed_password else 0}): {hashed_password[:50] if hashed_password else 'None'}...")
            print(f"[DEBUG] Tipo de hash: {type(hashed_password)}")
            import traceback
            traceback.print_exc()
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Genera el hash de la contraseña"""
        # Generar salt y hash con bcrypt
        salt = bcrypt.gensalt()
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def authenticate_user(self, username: str, password: str) -> Optional[Usuario]:
        """
        Autentica un usuario verificando sus credenciales
        Retorna el usuario si las credenciales son correctas, None en caso contrario
        """
        try:
            usuario = self.repository.get_by_username_or_id(username)
            if not usuario:
                print(f"Usuario '{username}' no encontrado")
                return None
            
            if not usuario.is_active:
                print(f"Usuario '{username}' está inactivo")
                return None
            
            # Debug: verificar hash
            print(f"[AUTH] Verificando contraseña para usuario: {usuario.id_usuario}")
            stored_hash = usuario.contraseña.strip() if usuario.contraseña else None
            print(f"[AUTH] Hash almacenado (longitud: {len(stored_hash) if stored_hash else 0}): {stored_hash[:30] if stored_hash else 'None'}...")
            print(f"[AUTH] Hash completo: {stored_hash}")
            print(f"[AUTH] Password recibida: '{password}'")
            print(f"[AUTH] Formato hash válido: {stored_hash.startswith('$2') if stored_hash else False}")
            
            if not stored_hash:
                print(f"[AUTH] No hay hash almacenado para usuario: {usuario.id_usuario}")
                return None
            
            if not self.verify_password(password, stored_hash):
                print(f"[AUTH] Contraseña incorrecta para usuario: {usuario.id_usuario}")
                # Intentar generar un nuevo hash para comparar (solo para debug)
                test_hash = self.get_password_hash(password)
                print(f"[AUTH] Hash generado para '{password}': {test_hash}")
                print(f"[AUTH] Los hashes son diferentes (esto es normal, cada hash es único)")
                return None
            
            print(f"Autenticación exitosa para usuario: {usuario.id_usuario}")
            return usuario
        except Exception as e:
            print(f"Error en authenticate_user: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def get(self, id_usuario: str) -> Optional[Usuario]:
        return self.repository.get_by_id_usuario(id_usuario)

    def get_by_nombre(self, nombre_usuario: str) -> Optional[Usuario]:
        return self.repository.get_by_nombre_usuario(nombre_usuario)

    def create(self, usuario_in: UsuarioCreate) -> Usuario:
        # Validar rol
        roles_validos = ['admin', 'jefe', 'servicios']
        if usuario_in.rol not in roles_validos:
            raise ValueError(f"Rol inválido: '{usuario_in.rol}'. Los roles válidos son: {', '.join(roles_validos)}")
        
        # Verificar si el usuario ya existe por ID
        existing_by_id = self.repository.get_by_id_usuario(usuario_in.id_usuario)
        if existing_by_id:
            raise ValueError(
                f"El usuario con ID '{usuario_in.id_usuario}' ya existe. "
                f"Usuario existente: {existing_by_id.nombre_usuario} (Rol: {existing_by_id.rol}). "
                f"Por favor, usa un ID diferente."
            )
        
        # Verificar si el nombre de usuario ya existe
        existing_by_nombre = self.repository.get_by_nombre_usuario(usuario_in.nombre_usuario)
        if existing_by_nombre:
            raise ValueError(
                f"El nombre de usuario '{usuario_in.nombre_usuario}' ya está en uso. "
                f"Usuario existente: {existing_by_nombre.id_usuario} (Rol: {existing_by_nombre.rol}). "
                f"Por favor, usa un nombre diferente."
            )
        
        # Normalizar id_carrera: convertir cadenas vacías a None
        id_carrera_normalizado = usuario_in.id_carrera
        if id_carrera_normalizado == '' or id_carrera_normalizado is None:
            id_carrera_normalizado = None
        
        # Validar que usuarios con rol 'servicios' no tengan carrera asignada
        if usuario_in.rol == 'servicios' and id_carrera_normalizado:
            raise ValueError("Los usuarios con rol 'servicios' no deben tener una carrera asignada. Por favor, deja el campo 'id_carrera' vacío.")
        
        # Validar que usuarios con rol 'jefe' tengan carrera asignada
        if usuario_in.rol == 'jefe' and not id_carrera_normalizado:
            raise ValueError("Los usuarios con rol 'jefe' deben tener una carrera asignada. Por favor, especifica un 'id_carrera'.")
        
        # Hashear la contraseña antes de guardarla
        usuario_data = usuario_in.dict()
        hashed_password = self.get_password_hash(usuario_data['contraseña'])
        
        # Crear el objeto Usuario directamente con la contraseña hasheada
        # No usar UsuarioCreate porque ya tiene la contraseña hasheada
        # Asegurar que id_carrera sea None para servicios, no cadena vacía
        id_carrera_final = None if usuario_in.rol == 'servicios' else id_carrera_normalizado
        db_usuario = Usuario(
            id_usuario=usuario_data['id_usuario'],
            nombre_usuario=usuario_data['nombre_usuario'],
            contraseña=hashed_password,
            id_carrera=id_carrera_final,
            rol=usuario_data['rol'],
            is_active=usuario_data.get('is_active', True)
        )
        
        self.repository.db.add(db_usuario)
        try:
            self.repository.db.commit()
            self.repository.db.refresh(db_usuario)
            return db_usuario
        except IntegrityError as e:
            self.repository.db.rollback()
            # Intentar obtener más información del error
            existing = self.repository.get_by_id_usuario(usuario_in.id_usuario)
            if existing:
                raise ValueError(
                    f"El usuario con ID '{usuario_in.id_usuario}' ya existe. "
                    f"Usuario existente: {existing.nombre_usuario} (Rol: {existing.rol}). "
                    f"Por favor, usa un ID diferente."
                )
            else:
                existing_nombre = self.repository.get_by_nombre_usuario(usuario_in.nombre_usuario)
                if existing_nombre:
                    raise ValueError(
                        f"El nombre de usuario '{usuario_in.nombre_usuario}' ya está en uso. "
                        f"Por favor, usa un nombre diferente."
                    )
            raise ValueError(f"Error de integridad al crear usuario: {str(e)}")
        except Exception as e:
            self.repository.db.rollback()
            raise ValueError(f"Error al crear usuario: {str(e)}")

    def update(self, id_usuario: str, usuario_update: UsuarioUpdate) -> Optional[Usuario]:
        # Obtener el usuario existente
        db_usuario = self.repository.get_by_id_usuario(id_usuario)
        if not db_usuario:
            return None
        
        update_data = usuario_update.dict(exclude_unset=True)
        
        # Normalizar id_carrera: convertir cadenas vacías a None
        if 'id_carrera' in update_data:
            if update_data['id_carrera'] == '' or update_data['id_carrera'] is None:
                update_data['id_carrera'] = None
        
        # Validar que usuarios con rol 'servicios' no tengan carrera asignada
        nuevo_rol = update_data.get('rol', db_usuario.rol)
        nuevo_id_carrera = update_data.get('id_carrera', db_usuario.id_carrera)
        
        if nuevo_rol == 'servicios' and nuevo_id_carrera:
            raise ValueError("Los usuarios con rol 'servicios' no deben tener una carrera asignada.")
        
        if nuevo_rol == 'jefe' and not nuevo_id_carrera:
            raise ValueError("Los usuarios con rol 'jefe' deben tener una carrera asignada.")
        
        # Si se actualiza la contraseña, hashearla
        if 'contraseña' in update_data and update_data['contraseña']:
            update_data['contraseña'] = self.get_password_hash(update_data['contraseña'])
        
        # Asegurar que id_carrera sea None para servicios
        if 'rol' in update_data and update_data['rol'] == 'servicios':
            update_data['id_carrera'] = None
        
        # Actualizar los campos
        for field, value in update_data.items():
            setattr(db_usuario, field, value)
        
        try:
            self.repository.db.commit()
            self.repository.db.refresh(db_usuario)
            return db_usuario
        except Exception as e:
            self.repository.db.rollback()
            raise ValueError(f"Error al actualizar usuario: {str(e)}")

    def delete(self, id_usuario: str, current_user_id: str = None) -> Optional[Usuario]:
        db_usuario = self.repository.get_by_id_usuario(id_usuario)
        if not db_usuario:
            return None
        
        # Validar que no se elimine a sí mismo (ya validado en el endpoint, pero doble validación)
        if current_user_id and current_user_id == id_usuario:
            raise ValueError("No puedes eliminarte a ti mismo")
        
        # Validar que no se elimine el último administrador
        if db_usuario.rol == 'admin':
            admins = self.repository.get_by_rol('admin', skip=0, limit=1000)
            admins_activos = [a for a in admins if a.is_active]
            
            if len(admins_activos) <= 1:
                raise ValueError("No se puede eliminar el último administrador del sistema. Debe haber al menos un administrador activo.")
        
        try:
            self.repository.db.delete(db_usuario)
            self.repository.db.commit()
            return db_usuario
        except ValueError:
            raise
        except Exception as e:
            self.repository.db.rollback()
            raise ValueError(f"Error al eliminar usuario: {str(e)}")

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all(skip, limit)

    def get_by_rol(self, rol: str, skip: int = 0, limit: int = 100):
        return self.repository.get_by_rol(rol, skip, limit)

    def reset_password_by_id(self, id_usuario: str, new_password: str) -> None:
        """Resetea la contraseña de un usuario por id (hash y guarda en la misma BD)."""
        usuario = self.repository.get_by_id_usuario(id_usuario)
        if not usuario:
            raise ValueError(f"Usuario '{id_usuario}' no encontrado")
        usuario.contraseña = self.get_password_hash(new_password)
        self.repository.db.commit()
        self.repository.db.refresh(usuario)
