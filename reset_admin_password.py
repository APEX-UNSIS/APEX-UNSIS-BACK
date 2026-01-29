#!/usr/bin/env python3
"""
Script para resetear la contraseña del usuario admin.
Uso: python reset_admin_password.py [nueva_contraseña]
Si no se proporciona contraseña, se usará 'admin123'
"""

import sys
import bcrypt
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar .env (esta carpeta o raíz APEX)
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_password_hash(password: str) -> str:
    """Genera el hash de la contraseña usando bcrypt"""
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def reset_admin_password(new_password: str = 'admin123'):
    """Resetea la contraseña del usuario admin"""
    # DB_* o POSTGRES_* (misma BD que usa la app)
    db_host = os.getenv('DB_HOST') or os.getenv('POSTGRES_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_user = os.getenv('DB_USER') or os.getenv('POSTGRES_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD') or os.getenv('POSTGRES_PASSWORD', '')
    db_name = os.getenv('DB_NAME') or os.getenv('POSTGRES_DB', 'apex_db')
    
    # Crear conexión
    database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    try:
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Generar hash de la nueva contraseña
        hashed_password = get_password_hash(new_password)
        
        # Actualizar la contraseña del admin
        result = session.execute(
            text("UPDATE usuarios SET contraseña = :password WHERE id_usuario = 'admin'"),
            {"password": hashed_password}
        )
        
        session.commit()
        
        if result.rowcount > 0:
            print(f"✅ Contraseña del usuario 'admin' reseteada exitosamente.")
            print(f"   Nueva contraseña: {new_password}")
            print(f"   Hash generado: {hashed_password}")
        else:
            print("⚠️  No se encontró el usuario 'admin' en la base de datos.")
            print("   Asegúrate de que el usuario existe.")
        
        session.close()
        
    except Exception as e:
        print(f"❌ Error al resetear la contraseña: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Obtener nueva contraseña de los argumentos o usar la predeterminada
    new_password = sys.argv[1] if len(sys.argv) > 1 else 'admin123'
    
    print("=" * 60)
    print("Script para Resetear Contraseña del Usuario Admin")
    print("=" * 60)
    print(f"Reseteando contraseña a: {new_password}")
    print()
    
    reset_admin_password(new_password)
    
    print()
    print("=" * 60)
