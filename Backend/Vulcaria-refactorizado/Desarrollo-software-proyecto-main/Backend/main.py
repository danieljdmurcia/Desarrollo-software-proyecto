from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from Backend import models
from Backend.database import engine, SessionLocal
from Backend.schemas import ProductoSchema, PedidoCreateSchema
from Backend.auth_schemas import RegistroSchema, LoginSchema, RecuperarSchema, ResetPasswordSchema

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
def actualizar_producto(id: int, producto: ProductoSchema, servicio=Depends(get_producto_service)):
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
def crear_pedido(pedido: PedidoCreateSchema, servicio: PedidoService = Depends(get_pedido_service)):
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
def actualizar_estado_pedido(
    id: int,
    estado: str,
    servicio: PedidoService = Depends(get_pedido_service)
):
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