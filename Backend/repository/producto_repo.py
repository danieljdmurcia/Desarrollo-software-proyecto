from sqlalchemy.orm import Session
from typing import Optional, List
from Backend import models
from Backend.repository.interfaces import IProductoRepository


class SQLAlchemyProductoAdapter(IProductoRepository):

    def __init__(self, db: Session):
        self._db = db

    def obtener_todos(self) -> List:
        return self._db.query(models.Producto).all()

    def obtener_por_id(self, id: int) -> Optional[models.Producto]:
        return self._db.query(models.Producto).filter(models.Producto.id == id).first()

    def crear(self, datos: dict) -> models.Producto:
        nuevo = models.Producto(**datos)
        self._db.add(nuevo)
        self._db.commit()
        self._db.refresh(nuevo)
        return nuevo

    def actualizar(self, id: int, datos: dict) -> Optional[models.Producto]:
        item = self.obtener_por_id(id)
        if item:
            item.nombre     = datos["nombre"]
            item.precio     = datos["precio"]
            item.disponible = datos["disponible"]
            self._db.commit()
            self._db.refresh(item)
        return item

    def eliminar(self, id: int) -> Optional[models.Producto]:
        item = self.obtener_por_id(id)
        if item:
            self._db.delete(item)
            self._db.commit()
        return item
