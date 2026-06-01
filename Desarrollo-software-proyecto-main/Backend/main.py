import os, shutil, secrets
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Header
from fastapi.staticfiles import StaticFiles
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

os.makedirs("images/productos", exist_ok=True)
app.mount("/images", StaticFiles(directory="images"), name="images")

# ── TOKEN DE ADMINISTRADOR ──────────────────────────────────────────────────
# Cámbialo por uno seguro. Puedes generarlo con: python -c "import secrets; print(secrets.token_hex(32))"
ADMIN_TOKEN = os.environ.get("VULCARIA_ADMIN_TOKEN", "vulcaria-admin-2024-token-seguro")

def verificar_admin(x_admin_token: str = Header(None)):
    """Dependencia que protege los endpoints de escritura."""
    if x_admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Token de administrador inválido o ausente")

# ── DB ──────────────────────────────────────────────────────────────────────
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── ENDPOINTS PÚBLICOS ──────────────────────────────────────────────────────
@app.get("/")
def home():
    return {"mensaje": "API Vulcaria 🚀"}

@app.get("/catalogo")
def catalogo(tipo: str = None, material: str = None,
             para_quien: str = None, orden: str = None,
             db: Session = Depends(get_db)):
    return producto_service.obtener_catalogo(db, tipo, material, para_quien, orden)

@app.get("/productos")
def obtener_productos(orden: str = None, db: Session = Depends(get_db)):
    return producto_service.obtener_todos(db, orden)

@app.get("/productos/{id}")
def obtener_producto(id: int, db: Session = Depends(get_db)):
    item = producto_service.obtener_por_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item

# ── FIX #1: imagen ANTES de /{id} para que FastAPI no la confunda ───────────
@app.post("/productos/imagen", dependencies=[Depends(verificar_admin)])
async def subir_imagen(file: UploadFile = File(...)):
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ("jpg", "jpeg", "png", "webp"):
        raise HTTPException(status_code=400, detail="Formato no permitido")
    nombre_archivo = f"{os.urandom(8).hex()}.{ext}"
    ruta = f"images/productos/{nombre_archivo}"
    with open(ruta, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"imagen_url": f"/images/productos/{nombre_archivo}"}

# ── ENDPOINTS PROTEGIDOS (requieren token de admin) ─────────────────────────
@app.post("/productos", dependencies=[Depends(verificar_admin)])
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    return producto_service.crear_producto(db, producto)

@app.put("/productos/{id}", dependencies=[Depends(verificar_admin)])
def actualizar_producto(id: int, producto: ProductoSchema, db: Session = Depends(get_db)):
    item = producto_service.actualizar_producto(db, id, producto)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item

@app.delete("/productos/{id}", dependencies=[Depends(verificar_admin)])
def desactivar_producto(id: int, db: Session = Depends(get_db)):
    item = producto_service.desactivar_producto(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto desactivado"}