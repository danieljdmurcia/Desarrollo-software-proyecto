from pydantic import BaseModel
import datetime


class ProductoSchema(BaseModel):
    nombre: str
    precio: float
    disponible: bool


class PedidoCreateSchema(BaseModel):
    producto_id: int
    cantidad: int


class PedidoResponseSchema(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    total: float
    estado: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True
