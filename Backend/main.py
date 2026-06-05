from fastapi import FastAPI, Request, Depends, HTTPException, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from Backend import models
from Backend.database import engine, SessionLocal
from Backend.schemas import ProductoSchema
from Backend.services import producto_service
from Backend.schemas import CitaSchema
from Backend.services import cita_service
from Backend.auth_schemas import RegistroSchema, LoginSchema, RecuperarSchema
from Backend.services.auth_service import AuthService, PRECIO_MINIMO
from Backend.repository import usuario_repo
import shutil, os, uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ── VISTAS ──
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

@app.get("/admin")
def admin_panel(request: Request):
    return templates.TemplateResponse(request, "admin.html")

# ── API PRODUCTOS ──
@app.get("/api/productos")
def obtener_productos(orden: str = None, db: Session = Depends(get_db)):
    return producto_service.obtener_todos(db, orden)

@app.post("/api/productos")
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    if producto.precio and producto.precio < PRECIO_MINIMO:
        raise HTTPException(status_code=400,
            detail=f"El precio mínimo permitido es ${PRECIO_MINIMO:,.0f} COP.")
    return producto_service.crear_producto(db, producto)

@app.get("/api/productos/{id}")
def obtener_producto(id: int, db: Session = Depends(get_db)):
    item = producto_service.obtener_por_id(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item

@app.put("/api/productos/{id}")
def actualizar_producto(id: int, producto: ProductoSchema, db: Session = Depends(get_db)):
    if producto.precio and producto.precio < PRECIO_MINIMO:
        raise HTTPException(status_code=400,
            detail=f"El precio mínimo permitido es ${PRECIO_MINIMO:,.0f} COP.")
    item = producto_service.actualizar_producto(db, id, producto)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item

@app.patch("/api/productos/{id}/suspender")
def suspender_producto(id: int, db: Session = Depends(get_db)):
    item = producto_service.suspender_producto(db, id)
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto suspendido"}

# ── SUBIDA DE IMÁGENES ──
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

@app.post("/api/upload-imagen")
async def upload_imagen(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes JPG, PNG, WEBP o GIF.")
    ext      = file.filename.rsplit(".", 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    dest     = os.path.join("static", "images", filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"url": f"/static/images/{filename}"}

# ── API CITAS ──
@app.get("/citas")
def citas(request: Request):
    return templates.TemplateResponse(request, "citas.html")

@app.post("/api/citas")
def crear_cita(cita: CitaSchema, db: Session = Depends(get_db)):
    resultado = cita_service.crear_cita(db, cita)
    if not resultado:
        raise HTTPException(status_code=400, detail="Hora no disponible")
    return resultado

@app.get("/api/citas/horas-libres")
def horas_libres(fecha: str, servicio: str, db: Session = Depends(get_db)):
    return cita_service.obtener_horas_libres(db, fecha, servicio)

# ── AUTH ──
auth_service = AuthService()

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@app.post("/api/auth/registro")
def registro(datos: RegistroSchema, db: Session = Depends(get_db)):
    try:
        return auth_service.registrar(db, datos.nombre, datos.usuario, datos.email, datos.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login")
def login(datos: LoginSchema, db: Session = Depends(get_db)):
    try:
        return auth_service.login(db, datos.email, datos.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/api/auth/recuperar")
async def recuperar(datos: RecuperarSchema, db: Session = Depends(get_db)):
    return await auth_service.solicitar_recuperacion(db, datos.email)