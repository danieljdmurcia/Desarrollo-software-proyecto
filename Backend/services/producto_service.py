<<<<<<< HEAD
from typing import Optional, List
from Backend.repository.interfaces import IProductoRepository
from Backend.services.interfaces import IProductoService
from Backend.strategies import OrdenStrategyFactory, FiltrarDisponibles


class ProductoServiceImpl(IProductoService):

    def __init__(self, repo: IProductoRepository):
        self._repo = repo

    def obtener_todos(self, orden: str = None, filtro: str = None) -> List:
        productos = self._repo.obtener_todos()

        if filtro == "disponibles":
            productos = FiltrarDisponibles().filtrar(productos)

        estrategia = OrdenStrategyFactory.create(orden)
        if estrategia:
            productos = estrategia.ordenar(productos)

        return productos

    def obtener_por_id(self, id: int) -> Optional[object]:
        return self._repo.obtener_por_id(id)

    def crear_producto(self, datos: dict) -> object:
        return self._repo.crear(datos)

    def actualizar_producto(self, id: int, datos: dict) -> Optional[object]:
        return self._repo.actualizar(id, datos)

    def eliminar_producto(self, id: int) -> Optional[object]:
        return self._repo.eliminar(id)
=======
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
>>>>>>> origin/main
