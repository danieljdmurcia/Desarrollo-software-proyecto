from abc import ABC, abstractmethod
from typing import Optional, List


class IProductoService(ABC):

    @abstractmethod
    def obtener_todos(self, orden: str = None, filtro: str = None) -> List:
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[object]:
        pass

    @abstractmethod
    def crear_producto(self, datos: dict) -> object:
        pass

    @abstractmethod
    def actualizar_producto(self, id: int, datos: dict) -> Optional[object]:
        pass

    @abstractmethod
    def eliminar_producto(self, id: int) -> Optional[object]:
        pass
