from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

app = FastAPI(title="Inventario de dispositivos")


# Modelo de datos de los dispositivos
class Dispositivo(BaseModel):
    nombre: str
    tipo: str
    ip: str
    activo: bool = True

# Modelo para actualizar parcialmente un dispositivo
class DispositivoParcial(BaseModel):
    nombre: str | None = None
    tipo: str | None = None
    ip: str | None = None
    activo: bool | None = None    


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


# UPDATE: Reemplazar completamente un dispositivo
@app.put("/dispositivos/{nombre}")
async def reemplazar(nombre: str, datos: Dispositivo):

    # Buscar el dispositivo que se desea reemplazar
    equipo = buscar(nombre)

    # Comprobar si existe
    if equipo is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el equipo {nombre}"
        )

    # Reemplazar todos sus datos
    inventario[inventario.index(equipo)] = datos

    # Devolver el dispositivo actualizado
    return datos


# UPDATE: Modificar parcialmente un dispositivo
@app.patch("/dispositivos/{nombre}")
async def modificar(nombre: str, cambios: DispositivoParcial):

    # Buscar el dispositivo
    equipo = buscar(nombre)

    # Comprobar si existe
    if equipo is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el equipo {nombre}"
        )

    # Modificar únicamente los campos enviados
    for campo, valor in cambios.model_dump(exclude_unset=True).items():
        setattr(equipo, campo, valor)

    # Devolver el dispositivo modificado
    return equipo


# DELETE: Eliminar un dispositivo
@app.delete("/dispositivos/{nombre}", status_code=204)
async def eliminar(nombre: str):

    # Buscar el dispositivo
    equipo = buscar(nombre)

    # Comprobar si existe
    if equipo is None:
        raise HTTPException(
            status_code=404,
            detail=f"No existe el equipo {nombre}"
        )

    # Eliminar el dispositivo del inventario
    inventario.remove(equipo)

    # Devolver respuesta sin contenido
    return Response(status_code=204)
