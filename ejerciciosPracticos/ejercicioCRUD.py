from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import *
 
app = FastAPI()

listaProductos = []

class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: int
    categoria: str
    fechaCreacion: datetime
    fechaActualizacion: datetime

@app.get("/productos", response_model=List[Producto])
def get_products():
    return listaProductos

@app.post("/productos/", response_model=Producto)
def crear_producto(producto: Producto):
    #producto = Producto(id="prod-1", nombre="producto", descripcion="Producto uno", precio=20, categoria="Hogar", fechaCreacion=datetime.now(),fechaActualizacion=datetime.now())
    listaProductos.append(producto)
    return producto

@app.get("/productos/{id}")
def get_producto(id: int):
    for n in range(0, len(listaProductos)):
        if listaProductos[n].id == id:
            return listaProductos[n]
        else:
            return 0
        
@app.put("/productos/{id}", response_model=Producto)
def update_producto(id: int, producto: Producto):
    listaProductos[id] = producto
    return producto


@app.delete("/productos/{id}")
def update_producto(id: int):
    del listaProductos[id]
    return {"mensaje": "Producto eliminado exitosamente."}
