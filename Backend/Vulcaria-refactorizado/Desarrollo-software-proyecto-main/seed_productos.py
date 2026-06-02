import sys
sys.path.insert(0, '.')

from Backend.database import SessionLocal, engine
from Backend import models

models.Base.metadata.create_all(bind=engine)

productos = [
    {"nombre": "Anillo de compromiso clásico",    "precio": 1200000, "disponible": True, "imagen_url": "/images/anillo1-removebg-preview.png"},
    {"nombre": "Anillo de compromiso moderno",     "precio": 980000,  "disponible": True, "imagen_url": "/images/anillo2-removebg-preview.png"},
    {"nombre": "Anillo de compromiso elegante",    "precio": 1450000, "disponible": True, "imagen_url": "/images/anillo3-removebg-preview.png"},
    {"nombre": "Anillo de compromiso minimalista", "precio": 850000,  "disponible": True, "imagen_url": "/images/anillo4-removebg-preview.png"},
    {"nombre": "Aretes de esmeralda",              "precio": 760000,  "disponible": True, "imagen_url": "/images/aretes1-removebg-preview.png"},
]

db = SessionLocal()
for p in productos:
    existe = db.query(models.Producto).filter(models.Producto.nombre == p["nombre"]).first()
    if not existe:
        db.add(models.Producto(**p))
db.commit()
db.close()
print("Productos creados correctamente")