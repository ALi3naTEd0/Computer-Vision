# Sistema de Inicio de Sesión Seguro con Verificación Facial

Sistema de autenticación biométrica que permite a los usuarios registrarse e iniciar sesión utilizando reconocimiento facial. Desarrollado con **DeepFace** y **OpenCV**, el sistema captura el rostro del usuario a través de la cámara web (o cargando una imagen) y lo compara contra el rostro registrado para conceder o denegar el acceso.

## Características

- **Registro de usuarios** con captura facial vía cámara web o carga de imagen
- **Inicio de sesión** mediante verificación biométrica facial con DeepFace
- **Detección de rostros en tiempo real** con retroalimentación visual (OpenCV + Haar Cascades)
- **Gestión de usuarios**: listar y eliminar cuentas registradas
- Base de datos ligera en formato JSON

## Requisitos previos

- Python 3.10 - 3.12 (TensorFlow no soporta Python 3.13+)
- Cámara web (opcional: también se pueden cargar imágenes desde archivo)

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Computer-Vision
```

### 2. Crear entorno virtual e instalar dependencias

> **Importante:** TensorFlow **no soporta Python 3.13+**. Si tu sistema tiene Python 3.13 o superior (como Arch Linux con 3.14), necesitas crear el venv con Python 3.12 usando `uv`.

**Arch Linux / sistemas con Python 3.13+:**

```bash
# Instalar uv (si no lo tienes)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Crear venv con Python 3.12 (uv lo descarga automáticamente)
uv venv --python 3.12 --seed .venv

# Instalar dependencias
.venv/bin/pip install -r requirements.txt
```

**Ubuntu / macOS / sistemas con Python 3.10-3.12:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> **Nota:** La primera ejecución descargará automáticamente los modelos de DeepFace (~500 MB). Esto solo ocurre una vez.

## Uso

Ejecuta la aplicación desde la raíz del proyecto:

```bash
python app.py
```

### Menú principal

Al ejecutar, se presenta un menú interactivo con las siguientes opciones:

| Opción | Descripción |
|--------|-------------|
| 1 | **Registrar nuevo usuario** — Captura tu rostro y lo asocia a un nombre de usuario |
| 2 | **Iniciar sesión** — Verifica tu identidad facial contra tu registro |
| 3 | **Ver usuarios registrados** — Lista todos los usuarios en el sistema |
| 4 | **Eliminar usuario** — Elimina una cuenta y su imagen facial |
| 5 | **Salir** — Cierra la aplicación |

### Flujo de registro

1. Selecciona la opción **1** del menú
2. Ingresa un nombre de usuario (solo letras y números)
3. Elige cómo proporcionar tu imagen facial:
   - **Cámara web**: Se abre una ventana con la cámara. Un recuadro verde indica que se detecta tu rostro. Presiona `c` para capturar o `q` para cancelar.
   - **Archivo**: Ingresa la ruta completa de una imagen con tu rostro (JPG, PNG)
4. El sistema guarda tu rostro y confirma el registro

### Flujo de inicio de sesión

1. Selecciona la opción **2** del menú
2. Ingresa tu nombre de usuario
3. Proporciona una nueva imagen facial (cámara o archivo)
4. DeepFace compara ambos rostros y muestra el resultado:
   - **ACCESO CONCEDIDO**: Los rostros coinciden, se simula una sesión activa
   - **ACCESO DENEGADO**: Los rostros no coinciden, se muestra la distancia facial

## Estructura del proyecto

```
Computer-Vision/
├── app.py                  # Aplicación principal (punto de entrada)
├── src/
│   ├── __init__.py
│   ├── db.py               # Módulo de base de datos (JSON)
│   └── face_manager.py     # Captura y verificación facial (DeepFace + OpenCV)
├── data/                   # (se crea automáticamente)
│   ├── users.json          # Base de datos de usuarios
│   └── faces/              # Imágenes faciales almacenadas
├── requirements.txt
├── README.md
└── LICENSE
```

## Tecnologías utilizadas

- **[DeepFace](https://github.com/serengil/deepface)** — Framework de reconocimiento facial (verificación con modelo VGG-Face)
- **[OpenCV](https://opencv.org/)** — Captura de video y detección de rostros en tiempo real
- **Python 3** — Lenguaje de programación