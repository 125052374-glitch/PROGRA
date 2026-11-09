from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Inventario de dispositivos")


# Modelo de datos de los dispositivos
class Dispositivo(BaseModel):
    nombre: str
    tipo: str
    ip: str
    activo: bool = True


# Base de datos simulada
inventario = [
    Dispositivo(nombre="R1", tipo="Router", ip="192.168.1.1"),
    Dispositivo(nombre="SW1", tipo="Switch", ip="192.168.1.2"),
    Dispositivo(nombre="SRV1", tipo="Servidor", ip="192.168.1.3")
]


# Función para buscar un dispositivo por su nombre
def buscar(nombre: str) -> Dispositivo | None:
    for equipo in inventario:
        if equipo.nombre.upper() == nombre.upper():
            return equipo
    return None


# READ: Obtener todos los dispositivos
@app.get("/dispositivos")
async def listar():
    return inventario


# READ: Obtener un dispositivo por nombre
@app.get("/dispositivos/{nombre}")
async def obtener(nombre: str):
    equipo = buscar(nombre)

    if equipo is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el equipo {nombre}"
        )

    return equipo


# CREATE: Registrar un nuevo dispositivo
@app.post("/dispositivos", status_code=201)
async def crear(nuevo: Dispositivo):

    # Verificar si el dispositivo ya existe
    if buscar(nuevo.nombre) is not None:
        raise HTTPException(
            status_code=409,
            detail=f"Ya existe el equipo {nuevo.nombre}"
        )

    # Agregar el dispositivo al inventario
    inventario.append(nuevo)

    # Devolver el dispositivo registrado
    return nuevo