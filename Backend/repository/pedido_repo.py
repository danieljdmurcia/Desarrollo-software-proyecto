from sqlalchemy.orm import Session
from typing import Optional, List
from Backend import models
from Backend.repository.interfaces import IPedidoRepository


class SQLAlchemyPedidoAdapter(IPedidoRepository):

    def __init__(self, db: Session):
        self._db = db

    def obtener_todos(self) -> List:
        return self._db.query(models.Pedido).all()

    def obtener_por_id(self, id: int) -> Optional[models.Pedido]:
        return self._db.query(models.Pedido).filter(models.Pedido.id == id).first()

    def obtener_producto_por_id(self, producto_id: int) -> Optional[models.Producto]:
        return self._db.query(models.Producto).filter(models.Producto.id == producto_id).first()

    def crear(self, datos: dict) -> models.Pedido:
        nuevo = models.Pedido(**datos)
        self._db.add(nuevo)
        self._db.commit()
        self._db.refresh(nuevo)
        return nuevo

    def actualizar_estado(self, id: int, estado: str) -> Optional[models.Pedido]:
        item = self.obtener_por_id(id)
        if item:
            item.estado = estado
            self._db.commit()
            self._db.refresh(item)
        return item

    def eliminar(self, id: int) -> Optional[models.Pedido]:
        item = self.obtener_por_id(id)
        if item:
            self._db.delete(item)
            self._db.commit()
        return item
