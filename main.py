from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductoSchema(BaseModel):
    nombre: str
    precio: float
    disponible: bool

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"mensaje": "API con MySQL funcionando 🚀"}

@app.get("/productos")
def obtener_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).all()

@app.post("/productos")
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    nuevo = models.Producto(**producto.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/productos/{id}")
def obtener_producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/productos/{id}")
def actualizar_producto(id: int, producto: ProductoSchema, db: Session = Depends(get_db)):
    item = db.query(models.Producto).filter(models.Producto.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    item.nombre = producto.nombre
    item.precio = producto.precio
    item.disponible = producto.disponible
    db.commit()
    db.refresh(item)
    return item

@app.delete("/productos/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    item = db.query(models.Producto).filter(models.Producto.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(item)
    db.commit()
    return {"mensaje": "Producto eliminado"}