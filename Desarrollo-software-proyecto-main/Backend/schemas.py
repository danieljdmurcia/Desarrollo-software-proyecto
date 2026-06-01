from pydantic import BaseModel
from typing import Optional

class ProductoSchema(BaseModel):
    nombre:      str
    descripcion: Optional[str] = ""
    precio:      float
    disponible:  bool = True
    tipo:        Optional[str] = ""
    material:    Optional[str] = ""
    para_quien:  Optional[str] = ""
    imagen_url:  Optional[str] = ""