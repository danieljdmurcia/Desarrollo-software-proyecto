from sqlalchemy import Column, Integer, String, Float, Boolean
from Backend.database import Base  

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    precio = Column(Float)
    disponible = Column(Boolean, default=True)

class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    cedula = Column(String, nullable=False)
    fecha_nacimiento = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    servicio = Column(String, nullable=False)
    fecha = Column(String, nullable=False)
    hora = Column(String, nullable=False)
    comentario = Column(String, nullable=True)
    estado = Column(String, default="pendiente")