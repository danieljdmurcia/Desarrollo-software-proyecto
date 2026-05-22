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
