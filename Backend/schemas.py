from pydantic import BaseModel

class ProductoSchema(BaseModel):
    nombre: str
    precio: float
    disponible: bool