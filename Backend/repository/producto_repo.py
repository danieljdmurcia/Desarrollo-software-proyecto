from sqlalchemy.orm import Session
from Backend import models

def obtener_todos(db: Session):
    return db.query(models.Producto).all()

def obtener_por_id(db: Session, id: int):
    return db.query(models.Producto).filter(models.Producto.id == id).first()

def crear(db: Session, datos: dict):
    nuevo = models.Producto(**datos)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def actualizar(db: Session, id: int, datos: dict):
    item = obtener_por_id(db, id)
    if item:
        item.nombre = datos["nombre"]
        item.precio = datos["precio"]
        item.disponible = datos["disponible"]
        db.commit()
        db.refresh(item)
    return item

def eliminar(db: Session, id: int):
    item = obtener_por_id(db, id)
    if item:
        db.delete(item)
        db.commit()
    return item