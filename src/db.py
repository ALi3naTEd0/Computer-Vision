"""
Módulo de base de datos de usuarios.
Almacena la información de usuarios registrados en un archivo JSON.
"""

import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "users.json")


def _ensure_db():
    """Crea el archivo de base de datos si no existe."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, "w") as f:
            json.dump({}, f)


def load_users() -> dict:
    """Carga y retorna el diccionario de usuarios registrados."""
    _ensure_db()
    with open(DB_PATH, "r") as f:
        return json.load(f)


def save_users(users: dict):
    """Guarda el diccionario de usuarios en disco."""
    _ensure_db()
    with open(DB_PATH, "w") as f:
        json.dump(users, f, indent=2)


def user_exists(username: str) -> bool:
    """Verifica si un nombre de usuario ya está registrado."""
    users = load_users()
    return username in users


def register_user(username: str, face_image_path: str):
    """Registra un nuevo usuario con la ruta a su imagen facial."""
    users = load_users()
    users[username] = {"face_path": face_image_path}
    save_users(users)


def get_user(username: str) -> dict | None:
    """Retorna la información de un usuario, o None si no existe."""
    users = load_users()
    return users.get(username)


def delete_user(username: str) -> bool:
    """Elimina un usuario. Retorna True si se eliminó, False si no existía."""
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
        return True
    return False
