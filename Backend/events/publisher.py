from typing import List
from Backend.events.interfaces import IObserver, IEventPublisher


class PedidoEventPublisher(IEventPublisher):

    def __init__(self):
        self._observers: List[IObserver] = []

    def suscribir(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def desuscribir(self, observer: IObserver) -> None:
        self._observers.remove(observer)

    def notificar(self, evento: str, datos: dict) -> None:
        for observer in self._observers:
            observer.update(evento, datos)
