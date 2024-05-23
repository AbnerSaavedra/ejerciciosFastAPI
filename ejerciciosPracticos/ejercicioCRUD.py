from fastapi import FastAPI
from pydantic import BaseModel
from datetime import *
 
app = FastAPI()

listaProductos = []

class Producto(BaseModel):
    id: str
    nombre: str
    descripcion: str
    precio: int
    categoria: str
    fechaCreacion: datetime
    fechaActualizacion: datetime

@app.get("/productos")
def get_products():
    return listaProductos

@app.post("/producto/")
def crear_producto()-> Producto:
    producto = Producto(id="prod-1", nombre="producto", descripcion="Producto uno", precio=20, categoria="Hogar", fechaCreacion=datetime.now(),fechaActualizacion=datetime.now())
    listaProductos.append(producto)
    return producto

@app.get("/producto/{id}")
def get_producto(id):
    for n in range(0, len(listaProductos)):
        if listaProductos[n].id == id:
            return listaProductos[n]
        else:
            return 0
        
@app.put("/producto/{id}")
def update_producto(id):
    producto = {}
    for n in range(0, len(listaProductos)):
        if listaProductos[n].id == id:
            producto = listaProductos[n]


@app.delete("/producto/{id}")
def update_producto(id):
    for n in range(0, len(listaProductos)):
        if listaProductos[n].id == id:
            listaProductos.remove(listaProductos[n])
