import logging
from Backend.events.interfaces import IObserver

logger = logging.getLogger(__name__)


class EmailObserver(IObserver):
   
    def update(self, evento: str, datos: dict) -> None:
        if evento == "PEDIDO_CREADO":
            logger.info(
                f"[EMAIL] Confirmación enviada "
                f"| Pedido #{datos.get('pedido_id')} "
                f"| Producto #{datos.get('producto_id')} "
                f"| Total: ${datos.get('total', 0):.2f}"
            )


class InventarioObserver(IObserver):

    def update(self, evento: str, datos: dict) -> None:
        if evento == "PEDIDO_CREADO":
            logger.info(
                f"[INVENTARIO] Stock descontado "
                f"| Producto #{datos.get('producto_id')} "
                f"| Cantidad: -{datos.get('cantidad')}"
            )
        elif evento == "PEDIDO_CANCELADO":
            logger.info(
                f"[INVENTARIO] Stock repuesto "
                f"| Producto #{datos.get('producto_id')} "
                f"| Cantidad: +{datos.get('cantidad')}"
            )


class StatsObserver(IObserver):

    def update(self, evento: str, datos: dict) -> None:
        if evento == "PEDIDO_CREADO":
            logger.info(
                f"[STATS] Venta registrada "
                f"| Total: ${datos.get('total', 0):.2f} "
                f"| Estado: {datos.get('estado')}"
            )
