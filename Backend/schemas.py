from pydantic import BaseModel
from typing import Optional
<<<<<<< HEAD
import datetime

=======
>>>>>>> origin/main

class ProductoSchema(BaseModel):
    nombre: str
    precio: float
    disponible: bool
<<<<<<< HEAD
    imagen_url: Optional[str] = None


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
=======
    unidades: Optional[int]   = 0       # ← nuevo: stock
    categoria: Optional[str]  = "general"  # ← nuevo: categoría
    imagen_url: Optional[str] = None    # ← nuevo: URL de imagen

class CitaSchema(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    fecha_nacimiento: str
    correo: str
    telefono: str
    servicio: str
    fecha: str
    hora: str
    comentario: str = None
>>>>>>> origin/main
