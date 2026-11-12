
"""Inventario de red — Práctica 3.

Alumno: Isaias Cruz
Matrícula: 125052374
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Inventario de red")


class Dispositivo(BaseModel):
    nombre: str
    tipo: str
    ip: str
    activo: bool = True


inventario = [
    Dispositivo(nombre="R1", tipo="router", ip="10.0.0.1"),
    Dispositivo(
        nombre="SW1",
        tipo="switch",
        ip="10.0.0.10",
        activo=False
    ),
    Dispositivo(
        nombre="FW1",
        tipo="firewall",
        ip="10.0.0.254"
    ),
]


@app.get("/")
async def estado():
    """Comprueba que el servicio responde."""
    return {
        "servicio": "Inventario de red",
        "total": len(inventario)
    }



@app.get("/dispositivos")
async def listar(activo: bool | None = None):
    """Lista el inventario. Con ?activo=true filtra los que están en línea."""
    if activo is None:
        return inventario
    return [equipo for equipo in inventario if equipo.activo == activo]



@app.get("/dispositivos/{nombre}")
async def obtener(nombre: str):
    """Busca un equipo por su nombre."""
    for equipo in inventario:
        if equipo.nombre.upper() == nombre.upper():
            return equipo

    raise HTTPException(
        status_code=404,
        detail=f"No existe el equipo {nombre}"
    )


# CREATE: Registrar un nuevo dispositivo
@app.post("/dispositivos", status_code=201)
async def crear(nuevo: Dispositivo):
    """Registra un dispositivo en el inventario."""

    # Comprobar si ya existe un equipo con ese nombre
    for equipo in inventario:
        if equipo.nombre.upper() == nuevo.nombre.upper():
            raise HTTPException(
                status_code=409,
                detail=f"Ya existe el equipo {nuevo.nombre}"
            )

    # Agregar el nuevo dispositivo
    inventario.append(nuevo)

    # Devolver los datos del dispositivo registrado
    return nuevo




# UPDATE: Reemplazar completamente un dispositivo
@app.put("/dispositivos/{nombre}")
async def reemplazar(nombre: str, datos: Dispositivo):
    """Reemplaza los datos de un dispositivo existente."""

    # Buscar el dispositivo por nombre
    for indice, equipo in enumerate(inventario):

        if equipo.nombre.upper() == nombre.upper():

            # Evitar nombres duplicados con otros dispositivos
            for otro in inventario:
                if otro is not equipo and otro.nombre.upper() == datos.nombre.upper():
                    raise HTTPException(
                        status_code=409,
                        detail=f"Ya existe el equipo {datos.nombre}"
                    )

            # Reemplazar completamente el dispositivo
            inventario[indice] = datos

            # Devolver los datos actualizados
            return datos

    # Si el dispositivo no existe
    raise HTTPException(
        status_code=404,
        detail=f"No existe el equipo {nombre}"
    )
