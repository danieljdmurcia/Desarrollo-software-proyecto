from sqlalchemy.orm import Session
from Backend import models

def obtener_todos(db: Session):
    return db.query(models.Producto).all()

def obtener_disponibles(db: Session):
    return db.query(models.Producto).filter(models.Producto.disponible == True).all()

def obtener_por_id(db: Session, id: int):
    return db.query(models.Producto).filter(models.Producto.id == id).first()

def filtrar(db: Session, tipo: str = None, material: str = None, para_quien: str = None):
    query = db.query(models.Producto).filter(models.Producto.disponible == True)
    if tipo:
        query = query.filter(models.Producto.tipo == tipo)
    if material:
        query = query.filter(models.Producto.material == material)
    if para_quien:
        query = query.filter(models.Producto.para_quien == para_quien)
    return query.all()

def crear(db: Session, datos: dict):
    nuevo = models.Producto(**datos)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def actualizar(db: Session, id: int, datos: dict):
    item = obtener_por_id(db, id)
    if item:
        for campo, valor in datos.items():
            setattr(item, campo, valor)
        db.commit()
        db.refresh(item)
    return item

def desactivar(db: Session, id: int):
    item = obtener_por_id(db, id)
    if item:
        item.disponible = False
        db.commit()
        db.refresh(item)
    return item