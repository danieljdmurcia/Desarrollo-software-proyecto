from sqlalchemy import Column, Integer, String, Float, Boolean
from Backend.database import Base  

class Producto(Base):
    __tablename__ = "productos"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(100))
    descripcion = Column(String(500), default="")
    precio      = Column(Float)
    disponible  = Column(Boolean, default=True)
    tipo        = Column(String(50), default="")
    material    = Column(String(50), default="")
    para_quien  = Column(String(50), default="")
    imagen_url  = Column(String(300), default="")