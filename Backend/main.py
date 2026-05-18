from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from Backend import models
from Backend.database import engine, SessionLocal
from Backend.schemas import ProductoSchema
from Backend.services import producto_service

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"mensaje": "API Vulcaria con SOLID 🚀"}

@app.get("/productos")
def obtener_productos(db: Session = Depends(get_db)):
    return producto_service.obtener_todos(db)

@app.post("/productos")
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    return producto_service.crear_producto(db, producto)

@app.get("/productos/{id}")
def obtener_producto(id: int, db: Session = Depends(get_db)):
    item = producto_service.obtener_por_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item

@app.put("/productos/{id}")
def actualizar_producto(id: int, producto: ProductoSchema, db: Session = Depends(get_db)):
    item = producto_service.actualizar_producto(db, id, producto)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item

@app.delete("/productos/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    item = producto_service.eliminar_producto(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}