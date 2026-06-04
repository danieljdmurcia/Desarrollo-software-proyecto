from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from Backend.security import hashear_password, verificar_password, crear_token
from Backend.repository import usuario_repo
from Backend.email_service import enviar_email_recuperacion
import secrets

DOMINIO_ADMIN = "vulcaria"
PRECIO_MINIMO = 200_000  # pesos colombianos


class AuthService:

    def registrar(self, db: Session, nombre: str, usuario: str, email: str, password: str):
        if usuario_repo.obtener_por_email(db, email):
            raise ValueError("Ya existe una cuenta con ese email")
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

        # Detectar si el correo es @vulcaria → es admin
        dominio = email.split("@")[-1].split(".")[0].lower()
        es_admin = dominio == DOMINIO_ADMIN

        hash_pw = hashear_password(password)
        nuevo = usuario_repo.crear_usuario(db, nombre, usuario, email, hash_pw, es_admin)
        token = crear_token({
            "sub": str(nuevo.id),
            "email": nuevo.email,
            "es_admin": nuevo.es_admin
        })
        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": {
                "id": nuevo.id,
                "nombre": nuevo.nombre,
                "usuario": nuevo.usuario,
                "email": nuevo.email,
                "es_admin": nuevo.es_admin
            }
        }

    def login(self, db: Session, email: str, password: str):
        usuario = usuario_repo.obtener_por_email(db, email)
        if not usuario or not verificar_password(password, usuario.password_hash):
            raise ValueError("Email o contraseña incorrectos")
        token = crear_token({
            "sub": str(usuario.id),
            "email": usuario.email,
            "es_admin": usuario.es_admin
        })
        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "email": usuario.email,
                "es_admin": usuario.es_admin
            }
        }

    async def solicitar_recuperacion(self, db: Session, email: str):
        usuario = usuario_repo.obtener_por_email(db, email)
        if not usuario:
            return {"mensaje": "Si el email existe, recibirás un enlace de recuperación"}
        token = secrets.token_urlsafe(32)
        expira = datetime.now(timezone.utc) + timedelta(hours=1)
        usuario_repo.guardar_reset_token(db, usuario, token, expira)
        try:
            await enviar_email_recuperacion(usuario.email, usuario.nombre, token)
        except Exception as e:
            print(f"ERROR EMAIL: {e}")
            raise
        return {"mensaje": "Si el email existe, recibirás un enlace de recuperación"}

    def resetear_password(self, db: Session, token: str, nueva_password: str):
        usuario = usuario_repo.obtener_por_reset_token(db, token)
        if not usuario:
            raise ValueError("Token inválido o expirado")
        if usuario.reset_token_expira < datetime.now(timezone.utc):
            raise ValueError("El token ha expirado, solicita uno nuevo")
        if len(nueva_password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        nuevo_hash = hashear_password(nueva_password)
        usuario_repo.actualizar_password(db, usuario, nuevo_hash)
        return {"mensaje": "Contraseña actualizada correctamente"}

    @staticmethod
    def validar_precio_admin(precio: float):
        """Restricción: ninguna joya puede venderse por menos de $200.000 COP."""
        if precio < PRECIO_MINIMO:
            raise ValueError(
                f"El precio mínimo permitido es ${PRECIO_MINIMO:,.0f} COP. "
                f"Precio ingresado: ${precio:,.0f} COP."
            )