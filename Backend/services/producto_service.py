from sqlalchemy.orm import Session
from Backend.repository import producto_repo
from Backend.schemas import ProductoSchema
from Backend.strategies import OrdenStrategy, OrdenarPorPrecio, OrdenarPorNombre, OrdenarPorDisponibilidad

def obtener_todos(db: Session, orden: str = None):
    productos = producto_repo.obtener_todos(db)
    estrategias = {
        "precio": OrdenarPorPrecio(),
        "nombre": OrdenarPorNombre(),
        "disponibilidad": OrdenarPorDisponibilidad()
    }
    if orden and orden in estrategias:
        return estrategias[orden].ordenar(productos)
    return productos

def obtener_por_id(db: Session, id: int):
    return producto_repo.obtener_por_id(db, id)

def obtener_por_categoria(db: Session, categoria: str):  # NUEVO
    return producto_repo.obtener_por_categoria(db, categoria)

def crear_producto(db: Session, producto: ProductoSchema):
    return producto_repo.crear(db, producto.dict())

def actualizar_producto(db: Session, id: int, producto: ProductoSchema):
    return producto_repo.actualizar(db, id, producto.dict())

def suspender_producto(db: Session, id: int):  # NUEVO — reemplaza eliminar_producto
    """Suspende un producto sin eliminarlo de la BD."""
    return producto_repo.suspender(db, id)