from abc import ABC, abstractmethod

class OrdenStrategy(ABC):
    @abstractmethod
    def ordenar(self, productos: list) -> list:
        pass

class OrdenarPorPrecio(OrdenStrategy):
    def ordenar(self, productos: list) -> list:
        return sorted(productos, key=lambda p: p.precio)

class OrdenarPorNombre(OrdenStrategy):
    def ordenar(self, productos: list) -> list:
        return sorted(productos, key=lambda p: p.nombre)

class OrdenarPorDisponibilidad(OrdenStrategy):
    def ordenar(self, productos: list) -> list:
        return sorted(productos, key=lambda p: not p.disponible)