
# Instrucciones — Inventario de red

## Requisitos
- Python 3.12 o superior
- Git
- Visual Studio Code

## Preparar el proyecto

1. Clonar el repositorio:
   git clone https://github.com/125052374-glitch/PROGRA.git

2. Entrar al proyecto:
   cd PROGRA

3. Crear el entorno virtual:
   python -m venv .venv

4. Activar el entorno en PowerShell:
   .\.venv\Scripts\Activate.ps1

5. Instalar las dependencias:
   python -m pip install -r requirements.txt

## Ejecutar la API

fastapi dev main.py

## Documentación interactiva

http://127.0.0.1:8000/docs

## Rutas disponibles

- GET / — Estado del servicio
- GET /dispositivos — Listado de dispositivos
- GET /dispositivos?activo=true — Dispositivos activos
- GET /dispositivos/{nombre} — Buscar por nombre

## Pruebas

- GET /dispositivos/R1 — HTTP 200
- GET /dispositivos/R99 — HTTP 404

