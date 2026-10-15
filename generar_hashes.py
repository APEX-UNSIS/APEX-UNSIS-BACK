"""
Script Python para generar contraseñas hasheadas con bcrypt
Útil para insertar usuarios manualmente en la base de datos
"""
import bcrypt


def hash_password(password: str) -> str:
    """Genera el hash bcrypt de una contraseña"""
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


if __name__ == "__main__":
    # Contraseñas de ejemplo
    passwords = {
        "admin123": "admin123",
        "jefe123": "jefe123",
        "servicios123": "servicios123"
    }
    
    print("=" * 80)
    print("HASHES DE CONTRASEÑAS PARA USUARIOS DE PRUEBA")
    print("=" * 80)
    print()
    
    for username, password in passwords.items():
        hashed = hash_password(password)
        print(f"Usuario: {username}")
        print(f"Contraseña: {password}")
        print(f"Hash: {hashed}")
        print("-" * 80)
        print()
    
    print("\nPara usar estos hashes, copia el valor del hash y pégalo en el campo 'contraseña'")
    print("de la tabla 'usuarios' en PostgreSQL.")
