from sqlalchemy.orm import Session
from Backend import models

def obtener_todos(db: Session):
    return db.query(models.Producto).all()

def obtener_por_id(db: Session, id: int):
    return db.query(models.Producto).filter(models.Producto.id == id).first()

def obtener_por_categoria(db: Session, categoria: str):  # NUEVO
    return db.query(models.Producto).filter(models.Producto.categoria == categoria).all()

def crear(db: Session, datos: dict):
    nuevo = models.Producto(**datos)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def actualizar(db: Session, id: int, datos: dict):
    item = obtener_por_id(db, id)
    if item:
        item.nombre     = datos["nombre"]
        item.precio     = datos["precio"]
        item.disponible = datos["disponible"]
        item.imagen_url = datos.get("imagen_url", item.imagen_url)  # NUEVO
        item.categoria  = datos.get("categoria", item.categoria)    # NUEVO
        db.commit()
        db.refresh(item)
    return item

def suspender(db: Session, id: int):  # NUEVO — reemplaza eliminar
    """Marca el producto como no disponible sin eliminarlo de la BD."""
    item = obtener_por_id(db, id)
    if item:
        item.disponible = False
        db.commit()
        db.refresh(item)
    return item