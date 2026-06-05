from pydantic import BaseModel
from typing import Optional

class ProductoSchema(BaseModel):
    nombre: str
    precio: float
    disponible: bool
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