<<<<<<< HEAD
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from Backend import models
from Backend.database import engine, SessionLocal
from Backend.schemas import ProductoSchema, PedidoCreateSchema
from Backend.auth_schemas import RegistroSchema, LoginSchema, RecuperarSchema, ResetPasswordSchema
from Backend.security import verificar_token

from Backend.repository.producto_repo import SQLAlchemyProductoAdapter
from Backend.services.producto_service import ProductoServiceImpl
from Backend.services.decorators import ValidacionDecorator, LoggingDecorator, AuditoriaDecorator
from Backend.services.pedido_service import PedidoService
from Backend.services.auth_service import AuthService

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Vulcaria API", description="Refactorización con patrones de diseño")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/Frontend", StaticFiles(directory="Frontend", html=True), name="frontend")
app.mount("/images", StaticFiles(directory="images"), name="images")

=======
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
>>>>>>> origin/main

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

<<<<<<< HEAD

def get_producto_service(db: Session = Depends(get_db)):
    repo     = SQLAlchemyProductoAdapter(db)
    servicio = ProductoServiceImpl(repo)
    servicio = ValidacionDecorator(servicio)
    servicio = LoggingDecorator(servicio)
    servicio = AuditoriaDecorator(servicio)
    return servicio


def get_pedido_service(db: Session = Depends(get_db)):
    return PedidoService(db)


def get_auth_service():
    return AuthService()


def get_usuario_actual(token: str, db: Session):
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    usuario_id = int(payload.get("sub"))
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return usuario


# ── Base ───────────────────────────────────────────────────────────────────────

@app.get("/")
def home():
    return {"mensaje": "API Vulcaria — Refactorización con patrones de diseño"}


# ── Auth ───────────────────────────────────────────────────────────────────────

@app.post("/auth/registro")
def registro(
    datos: RegistroSchema,
    db: Session = Depends(get_db),
    auth: AuthService = Depends(get_auth_service)
):
    try:
        return auth.registrar(db, datos.nombre, datos.email, datos.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login")
def login(
    datos: LoginSchema,
    db: Session = Depends(get_db),
    auth: AuthService = Depends(get_auth_service)
):
    try:
        return auth.login(db, datos.email, datos.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.post("/auth/recuperar-password")
async def recuperar_password(
    datos: RecuperarSchema,
    db: Session = Depends(get_db),
    auth: AuthService = Depends(get_auth_service)
):
    try:
        return await auth.solicitar_recuperacion(db, datos.email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/reset-password")
def reset_password(
    datos: ResetPasswordSchema,
    db: Session = Depends(get_db),
    auth: AuthService = Depends(get_auth_service)
):
    try:
        return auth.resetear_password(db, datos.token, datos.nueva_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Carrito ────────────────────────────────────────────────────────────────────

@app.get("/carrito")
def obtener_carrito(token: str, db: Session = Depends(get_db)):
    usuario = get_usuario_actual(token, db)
    items   = db.query(models.CarritoItem).filter(
        models.CarritoItem.usuario_id == usuario.id
    ).all()
    return [
        {
            "id":          item.id,
            "producto_id": item.producto_id,
            "nombre":      item.producto.nombre,
            "precio":      item.producto.precio,
            "imagen_url":  item.producto.imagen_url,
            "cantidad":    item.cantidad,
        }
        for item in items
    ]


@app.post("/carrito")
def agregar_al_carrito(producto_id: int, cantidad: int = 1,
                       token: str = "", db: Session = Depends(get_db)):
    usuario  = get_usuario_actual(token, db)
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    existing = db.query(models.CarritoItem).filter(
        models.CarritoItem.usuario_id  == usuario.id,
        models.CarritoItem.producto_id == producto_id
    ).first()

    if existing:
        existing.cantidad += cantidad
    else:
        db.add(models.CarritoItem(
            usuario_id=usuario.id,
            producto_id=producto_id,
            cantidad=cantidad
        ))
    db.commit()
    return {"mensaje": "Producto agregado al carrito"}


@app.patch("/carrito/{item_id}")
def actualizar_cantidad(item_id: int, cantidad: int,
                        token: str = "", db: Session = Depends(get_db)):
    usuario = get_usuario_actual(token, db)
    item    = db.query(models.CarritoItem).filter(
        models.CarritoItem.id         == item_id,
        models.CarritoItem.usuario_id == usuario.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    if cantidad <= 0:
        db.delete(item)
    else:
        item.cantidad = cantidad
    db.commit()
    return {"mensaje": "Cantidad actualizada"}


@app.delete("/carrito/{item_id}")
def eliminar_del_carrito(item_id: int, token: str = "",
                         db: Session = Depends(get_db)):
    usuario = get_usuario_actual(token, db)
    item    = db.query(models.CarritoItem).filter(
        models.CarritoItem.id         == item_id,
        models.CarritoItem.usuario_id == usuario.id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    db.delete(item)
    db.commit()
    return {"mensaje": "Producto eliminado del carrito"}


@app.delete("/carrito")
def vaciar_carrito(token: str = "", db: Session = Depends(get_db)):
    usuario = get_usuario_actual(token, db)
    db.query(models.CarritoItem).filter(
        models.CarritoItem.usuario_id == usuario.id
    ).delete()
    db.commit()
    return {"mensaje": "Carrito vaciado"}


# ── Productos ──────────────────────────────────────────────────────────────────

@app.get("/productos")
def obtener_productos(
    orden: str = None,
    filtro: str = None,
    servicio=Depends(get_producto_service)
):
    return servicio.obtener_todos(orden, filtro)


@app.post("/productos")
def crear_producto(producto: ProductoSchema, servicio=Depends(get_producto_service)):
    try:
        return servicio.crear_producto(producto.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/productos/{id}")
def obtener_producto(id: int, servicio=Depends(get_producto_service)):
    try:
        item = servicio.obtener_por_id(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item


@app.put("/productos/{id}")
def actualizar_producto(id: int, producto: ProductoSchema,
                        servicio=Depends(get_producto_service)):
    try:
        item = servicio.actualizar_producto(id, producto.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return item


@app.delete("/productos/{id}")
def eliminar_producto(id: int, servicio=Depends(get_producto_service)):
    try:
        item = servicio.eliminar_producto(id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not item:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}


# ── Pedidos ────────────────────────────────────────────────────────────────────

@app.get("/pedidos")
def obtener_pedidos(servicio: PedidoService = Depends(get_pedido_service)):
    return servicio.obtener_todos()


@app.post("/pedidos")
def crear_pedido(pedido: PedidoCreateSchema,
                 servicio: PedidoService = Depends(get_pedido_service)):
    try:
        return servicio.crear_pedido(pedido.producto_id, pedido.cantidad)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/pedidos/{id}")
def obtener_pedido(id: int, servicio: PedidoService = Depends(get_pedido_service)):
    item = servicio.obtener_por_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return item


@app.patch("/pedidos/{id}/estado")
def actualizar_estado_pedido(id: int, estado: str,
                              servicio: PedidoService = Depends(get_pedido_service)):
    try:
        item = servicio.actualizar_estado(id, estado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not item:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return item


@app.delete("/pedidos/{id}")
def eliminar_pedido(id: int, servicio: PedidoService = Depends(get_pedido_service)):
    item = servicio.eliminar_pedido(id)
    if not item:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"mensaje": "Pedido eliminado"}
=======
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
>>>>>>> origin/main
