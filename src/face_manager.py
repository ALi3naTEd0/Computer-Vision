"""
Módulo de gestión facial.
Maneja la captura de imágenes desde la cámara web y la verificación facial
utilizando DeepFace.
"""

import os
import cv2
from deepface import DeepFace

FACES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "faces")


def _ensure_faces_dir():
    """Crea el directorio de rostros si no existe."""
    os.makedirs(FACES_DIR, exist_ok=True)


def capture_face(username: str, prompt_msg: str = "Presiona 'c' para capturar tu rostro o 'q' para cancelar") -> str | None:
    """
    Captura una imagen del rostro del usuario desde la cámara web.

    Args:
        username: Nombre del usuario (para nombrar el archivo).
        prompt_msg: Mensaje a mostrar en la ventana de captura.

    Returns:
        Ruta al archivo de imagen capturado, o None si se canceló.
    """
    _ensure_faces_dir()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("\n[ERROR] No se pudo acceder a la cámara web.")
        print("Puedes usar la opción de cargar imagen desde archivo.\n")
        return None

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    print(f"\n{prompt_msg}")
    captured_path = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] No se pudo leer el frame de la cámara.")
            break

        # Detectar rostros para retroalimentación visual
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        display = frame.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if len(faces) == 0:
            cv2.putText(display, "No se detecta rostro", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(display, "Rostro detectado - Presiona 'c' para capturar", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Captura Facial", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("c"):
            if len(faces) > 0:
                image_path = os.path.join(FACES_DIR, f"{username}.jpg")
                cv2.imwrite(image_path, frame)
                captured_path = image_path
                print(f"[OK] Imagen capturada y guardada en: {image_path}")
                break
            else:
                print("[AVISO] No se detectó ningún rostro. Intenta de nuevo.")
        elif key == ord("q"):
            print("[INFO] Captura cancelada por el usuario.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return captured_path


def load_face_from_file(username: str) -> str | None:
    """
    Permite al usuario proporcionar la ruta a una imagen facial existente.
    Copia la imagen al directorio de rostros.

    Returns:
        Ruta al archivo copiado, o None si la ruta no es válida.
    """
    _ensure_faces_dir()

    image_path = input("Ingresa la ruta completa de la imagen facial: ").strip()
    if not os.path.isfile(image_path):
        print(f"[ERROR] El archivo '{image_path}' no existe.")
        return None

    # Verificar que la imagen se puede leer
    img = cv2.imread(image_path)
    if img is None:
        print("[ERROR] No se pudo leer la imagen. Asegúrate de que sea un formato válido.")
        return None

    dest_path = os.path.join(FACES_DIR, f"{username}.jpg")
    cv2.imwrite(dest_path, img)
    print(f"[OK] Imagen guardada en: {dest_path}")
    return dest_path


def verify_face(stored_image_path: str, live_image_path: str) -> dict:
    """
    Verifica si dos imágenes faciales pertenecen a la misma persona
    usando DeepFace.

    Args:
        stored_image_path: Ruta a la imagen facial almacenada del usuario.
        live_image_path: Ruta a la imagen facial capturada en el momento.

    Returns:
        Diccionario con el resultado de la verificación:
        {
            "verified": bool,
            "distance": float,
            "model": str,
            "message": str
        }
    """
    try:
        result = DeepFace.verify(
            img1_path=stored_image_path,
            img2_path=live_image_path,
            model_name="VGG-Face",
            enforce_detection=False,
        )
        return {
            "verified": result["verified"],
            "distance": result["distance"],
            "model": result["model"],
            "message": "Verificación exitosa" if result["verified"] else "Los rostros no coinciden",
        }
    except Exception as e:
        return {
            "verified": False,
            "distance": -1,
            "model": "N/A",
            "message": f"Error en la verificación: {str(e)}",
        }


def capture_temp_face() -> str | None:
    """
    Captura una imagen temporal para verificación de inicio de sesión.

    Returns:
        Ruta al archivo temporal, o None si se canceló.
    """
    _ensure_faces_dir()
    temp_path = os.path.join(FACES_DIR, "_temp_login.jpg")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("\n[ERROR] No se pudo acceder a la cámara web.")
        print("Puedes usar la opción de cargar imagen desde archivo.\n")
        return None

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    print("\nPresiona 'c' para capturar tu rostro para verificación o 'q' para cancelar")
    captured = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        display = frame.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(display, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if len(faces) == 0:
            cv2.putText(display, "No se detecta rostro", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            cv2.putText(display, "Rostro detectado - Presiona 'c'", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Verificacion Facial", display)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("c"):
            if len(faces) > 0:
                cv2.imwrite(temp_path, frame)
                captured = temp_path
                print("[OK] Imagen capturada para verificación.")
                break
            else:
                print("[AVISO] No se detectó ningún rostro.")
        elif key == ord("q"):
            print("[INFO] Verificación cancelada.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return captured


def load_temp_face_from_file() -> str | None:
    """
    Carga una imagen temporal desde archivo para verificación de login.

    Returns:
        Ruta al archivo temporal, o None si falla.
    """
    _ensure_faces_dir()
    temp_path = os.path.join(FACES_DIR, "_temp_login.jpg")

    image_path = input("Ingresa la ruta de la imagen facial para verificación: ").strip()
    if not os.path.isfile(image_path):
        print(f"[ERROR] El archivo '{image_path}' no existe.")
        return None

    img = cv2.imread(image_path)
    if img is None:
        print("[ERROR] No se pudo leer la imagen.")
        return None

    cv2.imwrite(temp_path, img)
    return temp_path


def cleanup_temp():
    """Elimina la imagen temporal de login si existe."""
    temp_path = os.path.join(FACES_DIR, "_temp_login.jpg")
    if os.path.exists(temp_path):
        os.remove(temp_path)
