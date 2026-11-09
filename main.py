from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Inventario")


# Modelo de datos
class Item(BaseModel):
    nombre: str
    precio: float
    cantidad: int


# Base de datos simulada
items = {}


# Ruta principal
@app.get("/")
def read_root():
    return {"Hello": "World"}


# CREATE - Crear un item
@app.post("/items/")
def create_item(item_id: int, item: Item):
    if item_id in items:
        raise HTTPException(status_code=400, detail="El item ya existe")

    items[item_id] = item

    return {
        "mensaje": "Item creado correctamente",
        "item_id": item_id,
        "item": item
    }


# READ - Obtener todos los items
@app.get("/items/")
def read_items():
    return items


# READ - Obtener un item por ID
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    return {
        "item_id": item_id,
        "item": items[item_id],
        "q": q
    }


# UPDATE - Actualizar un item
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    items[item_id] = item

    return {
        "mensaje": "Item actualizado correctamente",
        "item_id": item_id,
        "item": item
    }


# DELETE - Eliminar un item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item no encontrado")

    del items[item_id]

    return {
        "mensaje": "Item eliminado correctamente",
        "item_id": item_id
    }





#    .venv/
 #   __pycache__/
  #  .env
   # .Ds_Store
    #venv/