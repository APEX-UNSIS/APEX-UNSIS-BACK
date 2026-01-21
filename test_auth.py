#!/usr/bin/env python3
"""
Script para probar la autenticación JWT
Ejecuta: python test_auth.py
"""

import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def print_response(title, response):
    """Imprime una respuesta formateada"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)
    print(f"Status: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2, default=str, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print('='*60)


def test_login(username, password):
    """Prueba el endpoint de login"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "user": username,
        "password": password
    }
    
    print(f"\n🔐 Intentando login con usuario: {username}")
    response = requests.post(url, json=data)
    print_response(f"LOGIN - {username}", response)
    
    if response.status_code == 200:
        return response.json()["token"]
    return None


def test_get_current_user(token):
    """Prueba obtener el usuario actual"""
    url = f"{BASE_URL}/auth/me"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"\n👤 Obteniendo información del usuario actual...")
    response = requests.get(url, headers=headers)
    print_response("GET CURRENT USER", response)
    return response


def test_protected_endpoint(token):
    """Prueba un endpoint protegido (ejemplo)"""
    url = f"{BASE_URL}/ejemplo/protegido"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    print(f"\n🔒 Accediendo a endpoint protegido...")
    response = requests.get(url, headers=headers)
    print_response("ENDPOINT PROTEGIDO", response)
    return response


def test_without_token():
    """Prueba acceder sin token"""
    url = f"{BASE_URL}/auth/me"
    
    print(f"\n🚫 Intentando acceder sin token...")
    response = requests.get(url)
    print_response("ACCESO SIN TOKEN", response)
    return response


def test_public_endpoint():
    """Prueba un endpoint público"""
    url = f"{BASE_URL}/ejemplo/publico"
    
    print(f"\n🌍 Accediendo a endpoint público...")
    response = requests.get(url)
    print_response("ENDPOINT PÚBLICO", response)
    return response


def main():
    """Función principal"""
    print("\n" + "🚀 "*20)
    print("  PRUEBAS DE AUTENTICACIÓN JWT - APEX UNSIS")
    print("🚀 "*20)
    
    # Test 1: Login exitoso con admin
    print("\n\n" + "📝 "*20)
    print("  TEST 1: Login con credenciales correctas (admin)")
    print("📝 "*20)
    token_admin = test_login("admin", "admin123")
    
    if token_admin:
        # Test 2: Obtener usuario actual
        print("\n\n" + "📝 "*20)
        print("  TEST 2: Obtener información del usuario autenticado")
        print("📝 "*20)
        test_get_current_user(token_admin)
        
        # Test 3: Acceder a endpoint protegido
        print("\n\n" + "📝 "*20)
        print("  TEST 3: Acceder a endpoint protegido con token válido")
        print("📝 "*20)
        test_protected_endpoint(token_admin)
    
    # Test 4: Login con credenciales incorrectas
    print("\n\n" + "📝 "*20)
    print("  TEST 4: Login con credenciales incorrectas")
    print("📝 "*20)
    test_login("admin", "password_incorrecta")
    
    # Test 5: Acceder sin token
    print("\n\n" + "📝 "*20)
    print("  TEST 5: Acceder a endpoint protegido sin token")
    print("📝 "*20)
    test_without_token()
    
    # Test 6: Endpoint público
    print("\n\n" + "📝 "*20)
    print("  TEST 6: Acceder a endpoint público (sin autenticación)")
    print("📝 "*20)
    test_public_endpoint()
    
    # Test 7: Login con diferentes roles
    print("\n\n" + "📝 "*20)
    print("  TEST 7: Login con rol de Jefe")
    print("📝 "*20)
    token_jefe = test_login("jefe1", "jefe123")
    if token_jefe:
        test_get_current_user(token_jefe)
    
    print("\n\n" + "📝 "*20)
    print("  TEST 8: Login con rol de Servicios")
    print("📝 "*20)
    token_servicios = test_login("servicios1", "servicios123")
    if token_servicios:
        test_get_current_user(token_servicios)
    
    print("\n\n" + "✅ "*20)
    print("  PRUEBAS COMPLETADAS")
    print("✅ "*20 + "\n")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar al servidor.")
        print("Asegúrate de que el servidor esté ejecutándose en http://localhost:8000")
        print("Ejecuta: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
