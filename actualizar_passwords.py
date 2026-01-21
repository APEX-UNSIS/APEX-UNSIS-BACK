#!/usr/bin/env python3
"""
Script para actualizar las contraseñas de los usuarios de prueba
Genera hashes frescos y los actualiza en la base de datos
"""

from passlib.context import CryptContext
from sqlalchemy import create_engine, text
from app.config import settings

# Configurar bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Genera un hash bcrypt de la contraseña"""
    return pwd_context.hash(password)

def actualizar_passwords():
    """Actualiza las contraseñas de los usuarios de prueba"""
    
    # Crear conexión a la base de datos
    engine = create_engine(settings.DATABASE_URL)
    
    # Usuarios y contraseñas de prueba
    usuarios = [
        ('admin', 'admin123'),
        ('jefe1', 'jefe123'),
        ('jefe2', 'jefe123'),
        ('servicios1', 'servicios123'),
    ]
    
    print("\n" + "="*60)
    print("ACTUALIZANDO CONTRASEÑAS EN LA BASE DE DATOS")
    print("="*60 + "\n")
    
    with engine.connect() as conn:
        for id_usuario, password in usuarios:
            # Generar hash
            hashed = hash_password(password)
            
            # Actualizar en la BD
            result = conn.execute(
                text('UPDATE usuarios SET "contraseña" = :hash WHERE id_usuario = :id'),
                {"hash": hashed, "id": id_usuario}
            )
            
            conn.commit()
            
            if result.rowcount > 0:
                print(f"✓ Usuario '{id_usuario}' actualizado")
                print(f"  Password: {password}")
                print(f"  Hash: {hashed[:50]}...")
            else:
                print(f"✗ Usuario '{id_usuario}' NO ENCONTRADO en la base de datos")
            print()
    
    print("="*60)
    print("ACTUALIZACIÓN COMPLETADA")
    print("="*60)
    print("\nAhora puedes hacer login con:")
    print("  - admin / admin123")
    print("  - jefe1 / jefe123")
    print("  - jefe2 / jefe123")
    print("  - servicios1 / servicios123")
    print()

if __name__ == "__main__":
    actualizar_passwords()
