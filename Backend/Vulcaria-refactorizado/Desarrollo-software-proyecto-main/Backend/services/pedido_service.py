from sqlalchemy.orm import Session
from Backend.repository.pedido_repo import SQLAlchemyPedidoAdapter
from Backend.builders.pedido_builder import PedidoBuilder, PedidoDirector
from Backend.events.publisher import PedidoEventPublisher
from Backend.events.observers import EmailObserver, InventarioObserver, StatsObserver


class PedidoService:

    def __init__(self, db: Session):
        self._repo = SQLAlchemyPedidoAdapter(db)
        self._publisher = PedidoEventPublisher()
        self._publisher.suscribir(EmailObserver())
        self._publisher.suscribir(InventarioObserver())
        self._publisher.suscribir(StatsObserver())

    def obtener_todos(self):
        return self._repo.obtener_todos()

    def obtener_por_id(self, id: int):
        return self._repo.obtener_por_id(id)

    def crear_pedido(self, producto_id: int, cantidad: int):
        producto = self._repo.obtener_producto_por_id(producto_id)
        if not producto:
            raise ValueError(f"Producto con id={producto_id} no encontrado")
        if not producto.disponible:
            raise ValueError(f"El producto '{producto.nombre}' no está disponible")

        director = PedidoDirector(PedidoBuilder())
        pedido_data = director.construir_pedido_nuevo(producto_id, producto.precio, cantidad)
        pedido = self._repo.crear(pedido_data.to_dict())

        self._publisher.notificar("PEDIDO_CREADO", {
            "pedido_id":   pedido.id,
            "producto_id": pedido.producto_id,
            "cantidad":    pedido.cantidad,
            "total":       pedido.total,
            "estado":      pedido.estado,
        })

        return pedido

    def actualizar_estado(self, id: int, estado: str):
        pedido = self._repo.actualizar_estado(id, estado)
        if pedido and estado == "cancelado":
            self._publisher.notificar("PEDIDO_CANCELADO", {
                "pedido_id":   pedido.id,
                "producto_id": pedido.producto_id,
                "cantidad":    pedido.cantidad,
            })
        return pedido

    def eliminar_pedido(self, id: int):
        return self._repo.eliminar(id)
