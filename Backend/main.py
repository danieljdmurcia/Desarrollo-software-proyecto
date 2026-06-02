from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from Backend import models
from Backend.database import engine, SessionLocal
from Backend.schemas import ProductoSchema
from Backend.services import producto_service

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Conectar carpetas estáticas y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── VISTAS (páginas HTML) ──
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/catalogo")
def catalogo(request: Request, db: Session = Depends(get_db)):
    productos = producto_service.obtener_todos(db)
    return templates.TemplateResponse(request, "catalogo.html", {"productos": productos})

@app.get("/sobre-nosotros")
def sobre_nosotros(request: Request):
    return templates.TemplateResponse(request, "sobrenosotros.html")

@app.get("/servicios")
def servicios(request: Request):
    return templates.TemplateResponse(request, "servicios.html")

# ── API (datos JSON) ──
@app.get("/api/productos")
def obtener_productos(orden: str = None, db: Session = Depends(get_db)):
    return producto_service.obtener_todos(db, orden)

@app.post("/api/productos")
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    return producto_service.crear_producto(db, producto)

@app.get("/api/productos/{id}")
def obtener_producto(id: int, db: Session = Depends(get_db)):
    item = producto_service.obtener_por_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item

@app.put("/api/productos/{id}")
def actualizar_producto(id: int, producto: ProductoSchema, db: Session = Depends(get_db)):
    item = producto_service.actualizar_producto(db, id, producto)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item

@app.delete("/api/productos/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    item = producto_service.eliminar_producto(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}