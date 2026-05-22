from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from Backend.database import Base
import datetime

class Producto(Base):
    __tablename__ = "productos"

    id         = Column(Integer, primary_key=True, index=True)
    nombre     = Column(String(100))
    precio     = Column(Float)
    disponible = Column(Boolean, default=True)
    pedidos    = relationship("Pedido", back_populates="producto")


class Pedido(Base):
    __tablename__ = "pedidos"

    id          = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad    = Column(Integer)
    total       = Column(Float)
    estado      = Column(String(20), default="pendiente")
    created_at  = Column(DateTime, default=datetime.datetime.utcnow)
    producto    = relationship("Producto", back_populates="pedidos")
