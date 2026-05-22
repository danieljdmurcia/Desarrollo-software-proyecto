from abc import ABC, abstractmethod

class IObserver(ABC):
    @abstractmethod
    def update(self, evento: str, datos: dict) -> None:
        pass


class IEventPublisher(ABC):

    @abstractmethod
    def suscribir(self, observer: IObserver) -> None:
        pass

    @abstractmethod
    def desuscribir(self, observer: IObserver) -> None:
        pass

    @abstractmethod
    def notificar(self, evento: str, datos: dict) -> None:
        pass
