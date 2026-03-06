"""
Sistema de Inicio de Sesión Seguro con Verificación Facial
==========================================================

Aplicación principal que proporciona un menú interactivo para:
- Registrar nuevos usuarios con su rostro
- Iniciar sesión mediante verificación facial
- Administrar usuarios registrados
"""

import os
import sys

from src.db import user_exists, register_user, get_user, delete_user, load_users
from src.face_manager import (
    capture_face,
    load_face_from_file,
    verify_face,
    capture_temp_face,
    load_temp_face_from_file,
    cleanup_temp,
)

BANNER = """
╔══════════════════════════════════════════════════════╗
║   Sistema de Inicio de Sesión con Verificación      ║
║                    Facial                            ║
║                                                      ║
║   Seguridad biométrica con DeepFace                  ║
╚══════════════════════════════════════════════════════╝
"""

MENU = """
┌──────────────────────────────────┐
│         MENÚ PRINCIPAL           │
├──────────────────────────────────┤
│  1. Registrar nuevo usuario      │
│  2. Iniciar sesión               │
│  3. Ver usuarios registrados     │
│  4. Eliminar usuario             │
│  5. Salir                        │
└──────────────────────────────────┘
"""


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPresiona Enter para continuar...")


def get_image_method() -> str:
    """Pregunta al usuario cómo desea proporcionar la imagen facial."""
    print("\n¿Cómo deseas proporcionar tu imagen facial?")
    print("  1. Captura desde cámara web")
    print("  2. Cargar imagen desde archivo")
    choice = input("\nSelecciona (1/2): ").strip()
    return choice


def handle_register():
    """Flujo de registro de nuevo usuario."""
    print("\n── Registro de Nuevo Usuario ──\n")

    username = input("Ingresa un nombre de usuario: ").strip()
    if not username:
        print("[ERROR] El nombre de usuario no puede estar vacío.")
        return

    if not username.isalnum():
        print("[ERROR] El nombre de usuario solo puede contener letras y números.")
        return

    if user_exists(username):
        print(f"[ERROR] El usuario '{username}' ya está registrado.")
        return

    method = get_image_method()

    face_path = None
    if method == "1":
        face_path = capture_face(username)
    elif method == "2":
        face_path = load_face_from_file(username)
    else:
        print("[ERROR] Opción no válida.")
        return

    if face_path is None:
        print("[ERROR] No se pudo obtener la imagen facial. Registro cancelado.")
        return

    register_user(username, face_path)
    print(f"\n✓ Usuario '{username}' registrado exitosamente.")
    print("  Ahora puedes iniciar sesión usando verificación facial.")


def handle_login():
    """Flujo de inicio de sesión con verificación facial."""
    print("\n── Inicio de Sesión ──\n")

    username = input("Ingresa tu nombre de usuario: ").strip()
    if not username:
        print("[ERROR] El nombre de usuario no puede estar vacío.")
        return

    user = get_user(username)
    if user is None:
        print(f"[ERROR] El usuario '{username}' no está registrado.")
        return

    stored_face_path = user["face_path"]
    if not os.path.isfile(stored_face_path):
        print("[ERROR] La imagen facial registrada no se encuentra. Vuelve a registrarte.")
        return

    print(f"\nVerificando identidad de '{username}'...")

    method = get_image_method()

    live_face_path = None
    if method == "1":
        live_face_path = capture_temp_face()
    elif method == "2":
        live_face_path = load_temp_face_from_file()
    else:
        print("[ERROR] Opción no válida.")
        return

    if live_face_path is None:
        print("[ERROR] No se pudo obtener la imagen facial. Inicio de sesión cancelado.")
        return

    print("\nAnalizando rostro con DeepFace...")
    result = verify_face(stored_face_path, live_face_path)

    cleanup_temp()

    if result["verified"]:
        print(f"\n╔══════════════════════════════════════════╗")
        print(f"║  ✓ ACCESO CONCEDIDO                      ║")
        print(f"║  Bienvenido/a, {username:<24} ║")
        print(f"╚══════════════════════════════════════════╝")
        print(f"\n  Modelo utilizado: {result['model']}")
        print(f"  Distancia facial: {result['distance']:.4f}")

        # Simulación de sesión activa
        print("\n── Sesión Activa ──")
        print(f"  Usuario: {username}")
        print("  Estado: Conectado")
        print("  Acceso: Completo")
        input("\n  Presiona Enter para cerrar sesión...")
        print(f"\n  Sesión de '{username}' cerrada correctamente.")
    else:
        print(f"\n╔══════════════════════════════════════════╗")
        print(f"║  ✗ ACCESO DENEGADO                       ║")
        print(f"╚══════════════════════════════════════════╝")
        print(f"\n  Motivo: {result['message']}")
        if result['distance'] >= 0:
            print(f"  Distancia facial: {result['distance']:.4f}")
        print("  Los rostros no coinciden. Intenta de nuevo.")


def handle_list_users():
    """Muestra la lista de usuarios registrados."""
    print("\n── Usuarios Registrados ──\n")

    users = load_users()
    if not users:
        print("  No hay usuarios registrados.")
        return

    print(f"  {'#':<4} {'Usuario':<20} {'Imagen Facial'}")
    print(f"  {'─'*4} {'─'*20} {'─'*40}")
    for i, (username, data) in enumerate(users.items(), 1):
        face_status = "✓" if os.path.isfile(data["face_path"]) else "✗ (no encontrada)"
        print(f"  {i:<4} {username:<20} {face_status}")

    print(f"\n  Total: {len(users)} usuario(s)")


def handle_delete_user():
    """Flujo de eliminación de usuario."""
    print("\n── Eliminar Usuario ──\n")

    username = input("Ingresa el nombre del usuario a eliminar: ").strip()
    if not username:
        print("[ERROR] El nombre de usuario no puede estar vacío.")
        return

    user = get_user(username)
    if user is None:
        print(f"[ERROR] El usuario '{username}' no existe.")
        return

    confirm = input(f"¿Estás seguro de eliminar a '{username}'? (s/n): ").strip().lower()
    if confirm != "s":
        print("  Operación cancelada.")
        return

    # Eliminar imagen facial si existe
    face_path = user.get("face_path", "")
    if os.path.isfile(face_path):
        os.remove(face_path)

    delete_user(username)
    print(f"\n✓ Usuario '{username}' eliminado correctamente.")


def main():
    """Bucle principal de la aplicación."""
    print(BANNER)

    while True:
        print(MENU)
        choice = input("Selecciona una opción: ").strip()

        if choice == "1":
            handle_register()
            pause()
        elif choice == "2":
            handle_login()
            pause()
        elif choice == "3":
            handle_list_users()
            pause()
        elif choice == "4":
            handle_delete_user()
            pause()
        elif choice == "5":
            print("\n¡Hasta luego! 👋\n")
            sys.exit(0)
        else:
            print("\n[ERROR] Opción no válida. Intenta de nuevo.")
            pause()


if __name__ == "__main__":
    main()
