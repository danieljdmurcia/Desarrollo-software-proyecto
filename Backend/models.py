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
    imagen_url = Column(String(255), nullable=True)
    pedidos    = relationship("Pedido", back_populates="producto")
    carrito    = relationship("CarritoItem", back_populates="producto")


class Pedido(Base):
    __tablename__ = "pedidos"

    id          = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad    = Column(Integer)
    total       = Column(Float)
    estado      = Column(String(20), default="pendiente")
    created_at  = Column(DateTime, default=datetime.datetime.utcnow)
    producto    = relationship("Producto", back_populates="pedidos")


class Usuario(Base):
    __tablename__ = "usuarios"

    id                 = Column(Integer, primary_key=True, index=True)
    nombre             = Column(String(100), nullable=False)
    email              = Column(String(150), unique=True, index=True, nullable=False)
    password_hash      = Column(String(255), nullable=False)
    reset_token        = Column(String(255), nullable=True)
    reset_token_expira = Column(DateTime, nullable=True)
    intentos_fallidos  = Column(Integer, default=0)
    bloqueado_hasta    = Column(DateTime, nullable=True)
    created_at         = Column(DateTime, default=datetime.datetime.utcnow)
    carrito            = relationship("CarritoItem", back_populates="usuario")


class CarritoItem(Base):
    __tablename__ = "carrito"

    id          = Column(Integer, primary_key=True, index=True)
    usuario_id  = Column(Integer, ForeignKey("usuarios.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad    = Column(Integer, default=1)
    created_at  = Column(DateTime, default=datetime.datetime.utcnow)
    usuario     = relationship("Usuario", back_populates="carrito")
    producto    = relationship("Producto", back_populates="carrito")
    
