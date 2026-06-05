from abc import ABC, abstractmethod
from typing import Optional, List


class IProductoRepository(ABC):

    @abstractmethod
    def obtener_todos(self) -> List:
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[object]:
        pass

    @abstractmethod
    def crear(self, datos: dict) -> object:
        pass

    @abstractmethod
    def actualizar(self, id: int, datos: dict) -> Optional[object]:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> Optional[object]:
        pass


class IPedidoRepository(ABC):

    @abstractmethod
    def obtener_todos(self) -> List:
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[object]:
        pass

    @abstractmethod
    def obtener_producto_por_id(self, producto_id: int) -> Optional[object]:
        pass

    @abstractmethod
    def crear(self, datos: dict) -> object:
        pass

    @abstractmethod
    def actualizar_estado(self, id: int, estado: str) -> Optional[object]:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> Optional[object]:
        pass
