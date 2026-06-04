from pydantic import BaseModel

class ProductoSchema(BaseModel):
    nombre: str
    precio: float
    disponible: bool = True
    imagen_url: str = None   # NUEVO
    categoria: str = "general"  # NUEVO

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