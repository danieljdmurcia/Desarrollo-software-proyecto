from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    disponible: bool

productos = []

@app.get("/")
def home():
    return {"mensaje": "API funcionando en Azure 🚀"}

@app.get("/productos")
def obtener_productos():
    return productos

@app.post("/productos")
def crear_producto(producto: Producto):
    productos.append(producto.dict())
    return {"mensaje": "Producto creado"}

@app.get("/productos/{id}")
def obtener_producto(id: int):
    for producto in productos:
        if producto["id"] == id:
            return producto
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.get("/buscar")
def buscar_producto(disponible: bool = None):
    if disponible is None:
        return productos
    return [p for p in productos if p["disponible"] == disponible]