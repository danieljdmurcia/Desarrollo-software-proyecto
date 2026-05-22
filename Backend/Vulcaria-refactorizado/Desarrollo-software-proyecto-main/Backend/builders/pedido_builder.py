import datetime
from dataclasses import dataclass, field

@dataclass
class PedidoData:
    producto_id: int   = 0
    cantidad:    int   = 0
    total:       float = 0.0
    estado:      str   = "pendiente"
    created_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "producto_id": self.producto_id,
            "cantidad":    self.cantidad,
            "total":       self.total,
            "estado":      self.estado,
            "created_at":  self.created_at,
        }


class PedidoBuilder:
    def __init__(self):
        self._reset()

    def _reset(self):
        self._pedido          = PedidoData()
        self._precio_unitario = 0.0

    def set_producto(self, producto_id: int, precio_unitario: float) -> "PedidoBuilder":
        if producto_id <= 0:
            raise ValueError("El ID del producto debe ser un entero positivo")
        if precio_unitario <= 0:
            raise ValueError("El precio unitario debe ser mayor a 0")
        self._pedido.producto_id  = producto_id
        self._precio_unitario     = precio_unitario
        return self

    def set_cantidad(self, cantidad: int) -> "PedidoBuilder":
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        self._pedido.cantidad = cantidad
        return self

    def calcular_total(self) -> "PedidoBuilder":
        self._pedido.total = round(self._precio_unitario * self._pedido.cantidad, 2)
        return self

    def set_estado(self, estado: str) -> "PedidoBuilder":
        estados_validos = {"pendiente", "completado", "cancelado"}
        if estado not in estados_validos:
            raise ValueError(f"Estado '{estado}' inválido. Válidos: {estados_validos}")
        self._pedido.estado = estado
        return self

    def build(self) -> PedidoData:
        if not self._pedido.producto_id:
            raise ValueError("Debe especificar un producto antes de construir el pedido")
        if not self._pedido.cantidad:
            raise ValueError("Debe especificar la cantidad antes de construir el pedido")
        resultado = self._pedido
        self._reset()
        return resultado


class PedidoDirector:

    def __init__(self, builder: PedidoBuilder):
        self._builder = builder

    def construir_pedido_nuevo(
        self,
        producto_id:     int,
        precio_unitario: float,
        cantidad:        int
    ) -> PedidoData:
        return (
            self._builder
                .set_producto(producto_id, precio_unitario)
                .set_cantidad(cantidad)
                .calcular_total()
                .set_estado("pendiente")
                .build()
        )
