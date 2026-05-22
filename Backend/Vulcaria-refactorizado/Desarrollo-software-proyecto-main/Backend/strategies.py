from abc import ABC, abstractmethod
from typing import Optional


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


class OrdenStrategyFactory:
    _estrategias: dict = {
        "precio":         OrdenarPorPrecio,
        "nombre":         OrdenarPorNombre,
        "disponibilidad": OrdenarPorDisponibilidad,
    }

    @classmethod
    def create(cls, tipo: Optional[str]) -> Optional[OrdenStrategy]:
        if tipo and tipo in cls._estrategias:
            return cls._estrategias[tipo]()
        return None

    @classmethod
    def registrar(cls, tipo: str, estrategia: type) -> None:
        cls._estrategias[tipo] = estrategia

class FiltroStrategy(ABC):
    @abstractmethod
    def filtrar(self, productos: list) -> list:
        pass


class FiltrarDisponibles(FiltroStrategy):
    def filtrar(self, productos: list) -> list:
        return [p for p in productos if p.disponible]


class FiltrarPorRangoPrecio(FiltroStrategy):
    def __init__(self, minimo: float, maximo: float):
        self.minimo = minimo
        self.maximo = maximo

    def filtrar(self, productos: list) -> list:
        return [p for p in productos if self.minimo <= p.precio <= self.maximo]
