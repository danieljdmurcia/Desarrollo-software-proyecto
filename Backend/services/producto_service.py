from sqlalchemy.orm import Session
from Backend.repository import producto_repo
from Backend.schemas import ProductoSchema

def obtener_todos(db: Session):
    return producto_repo.obtener_todos(db)

def obtener_por_id(db: Session, id: int):
    return producto_repo.obtener_por_id(db, id)

def crear_producto(db: Session, producto: ProductoSchema):
    return producto_repo.crear(db, producto.dict())

def actualizar_producto(db: Session, id: int, producto: ProductoSchema):
    return producto_repo.actualizar(db, id, producto.dict())

def eliminar_producto(db: Session, id: int):
    return producto_repo.eliminar(db, id)