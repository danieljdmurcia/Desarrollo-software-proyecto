from sqlalchemy.orm import Session
from Backend.repository import producto_repo
from Backend.schemas import ProductoSchema
from Backend.strategies import OrdenarPorPrecio, OrdenarPorNombre, OrdenarPorDisponibilidad

def obtener_todos(db: Session, orden: str = None):
    productos = producto_repo.obtener_todos(db)
    estrategias = {
        "precio":         OrdenarPorPrecio(),
        "nombre":         OrdenarPorNombre(),
        "disponibilidad": OrdenarPorDisponibilidad()
    }
    if orden and orden in estrategias:
        return estrategias[orden].ordenar(productos)
    return productos

def obtener_catalogo(db: Session, tipo: str = None, material: str = None,
                     para_quien: str = None, orden: str = None):
    productos = producto_repo.filtrar(db, tipo, material, para_quien)
    estrategias = {
        "precio": OrdenarPorPrecio(),
        "nombre": OrdenarPorNombre(),
    }
    if orden and orden in estrategias:
        return estrategias[orden].ordenar(productos)
    return productos

def obtener_por_id(db: Session, id: int):
    return producto_repo.obtener_por_id(db, id)

def crear_producto(db: Session, producto: ProductoSchema):
    return producto_repo.crear(db, producto.dict())

def actualizar_producto(db: Session, id: int, producto: ProductoSchema):
    return producto_repo.actualizar(db, id, producto.dict())

def desactivar_producto(db: Session, id: int):
    return producto_repo.desactivar(db, id)