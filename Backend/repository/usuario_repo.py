from sqlalchemy.orm import Session
from datetime import datetime, timezone
from Backend.models import Usuario


def obtener_por_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()


def obtener_por_id(db: Session, usuario_id: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def obtener_por_reset_token(db: Session, token: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.reset_token == token).first()


def crear_usuario(db: Session, nombre: str, usuario: str, email: str, password_hash: str, es_admin: bool = False):
    # ← añadido es_admin con default False para no romper llamadas existentes
    nuevo = Usuario(
        nombre=nombre,
        usuario=usuario,
        email=email,
        password_hash=password_hash,
        es_admin=es_admin
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


def guardar_reset_token(db: Session, usuario: Usuario, token: str, expira: datetime):
    usuario.reset_token = token
    usuario.reset_token_expira = expira
    db.commit()


def actualizar_password(db: Session, usuario: Usuario, nuevo_hash: str):
    usuario.password_hash = nuevo_hash
    usuario.reset_token = None
    usuario.reset_token_expira = None
    db.commit()