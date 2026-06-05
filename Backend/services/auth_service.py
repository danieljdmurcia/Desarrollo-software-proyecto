from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Backend.security import hashear_password, verificar_password, crear_token
from Backend.repository import usuario_repo
from Backend.email_service import enviar_email_recuperacion
import secrets

<<<<<<< HEAD
MAX_INTENTOS    = 3
BLOQUEO_MINUTOS = 5
=======
DOMINIO_ADMIN = "vulcaria"
PRECIO_MINIMO = 200_000  # pesos colombianos
>>>>>>> origin/main


class AuthService:

    def registrar(self, db: Session, nombre: str, usuario: str, email: str, password: str):
        if usuario_repo.obtener_por_email(db, email):
            raise ValueError("Ya existe una cuenta con ese email")
        if len(password) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")

        # Verificar si el nombre de usuario ya existe
        if usuario_repo.obtener_por_usuario(db, usuario):
            raise ValueError("Ese nombre de usuario ya está en uso")

        # Detectar si el correo es @vulcaria → es admin
        dominio = email.split("@")[-1].split(".")[0].lower()
        es_admin = dominio == DOMINIO_ADMIN

        hash_pw = hashear_password(password)
<<<<<<< HEAD
        usuario = usuario_repo.crear_usuario(db, nombre, email, hash_pw)
        token   = crear_token({"sub": str(usuario.id), "email": usuario.email})
        return {
            "access_token": token,
            "token_type":   "bearer",
            "usuario": {"id": usuario.id, "nombre": usuario.nombre, "email": usuario.email}
=======
        try:
            nuevo = usuario_repo.crear_usuario(db, nombre, usuario, email, hash_pw, es_admin)
        except IntegrityError:
            db.rollback()
            raise ValueError("El nombre de usuario o correo ya está registrado")

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
>>>>>>> origin/main
        }

    def login(self, db: Session, email: str, password: str):
        usuario = usuario_repo.obtener_por_email(db, email)
        if not usuario:
            raise ValueError("Email o contraseña incorrectos")
<<<<<<< HEAD

        ahora = datetime.now(timezone.utc)

        if usuario.bloqueado_hasta:
            bloqueado_hasta = usuario.bloqueado_hasta
            if bloqueado_hasta.tzinfo is None:
                bloqueado_hasta = bloqueado_hasta.replace(tzinfo=timezone.utc)
            if ahora < bloqueado_hasta:
                segundos = int((bloqueado_hasta - ahora).total_seconds())
                minutos  = segundos // 60
                segs     = segundos % 60
                raise ValueError(
                    f"Cuenta bloqueada. Intenta de nuevo en {minutos}m {segs}s"
                )
            else:
                usuario.bloqueado_hasta   = None
                usuario.intentos_fallidos = 0
                db.commit()

        if not verificar_password(password, usuario.password_hash):
            usuario.intentos_fallidos += 1
            restantes = MAX_INTENTOS - usuario.intentos_fallidos

            if usuario.intentos_fallidos >= MAX_INTENTOS:
                usuario.bloqueado_hasta   = ahora + timedelta(minutes=BLOQUEO_MINUTOS)
                usuario.intentos_fallidos = 0
                db.commit()
                raise ValueError(
                    f"Demasiados intentos fallidos. Cuenta bloqueada por {BLOQUEO_MINUTOS} minutos"
                )

            db.commit()
            raise ValueError(
                f"Email o contraseña incorrectos. Te quedan {restantes} intento(s)"
            )

        usuario.intentos_fallidos = 0
        usuario.bloqueado_hasta   = None
        db.commit()

        token = crear_token({"sub": str(usuario.id), "email": usuario.email})
        return {
            "access_token": token,
            "token_type":   "bearer",
            "usuario": {"id": usuario.id, "nombre": usuario.nombre, "email": usuario.email}
=======
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
>>>>>>> origin/main
        }

    async def solicitar_recuperacion(self, db: Session, email: str):
        usuario = usuario_repo.obtener_por_email(db, email)
        if not usuario:
            return {"mensaje": "Si el email existe, recibirás un enlace de recuperación"}
        token  = secrets.token_urlsafe(32)
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
<<<<<<< HEAD
        usuario.intentos_fallidos = 0
        usuario.bloqueado_hasta   = None
        db.commit()
        return {"mensaje": "Contraseña actualizada correctamente"}
=======
        return {"mensaje": "Contraseña actualizada correctamente"}

    @staticmethod
    def validar_precio_admin(precio: float):
        """Restricción: ninguna joya puede venderse por menos de $200.000 COP."""
        if precio < PRECIO_MINIMO:
            raise ValueError(
                f"El precio mínimo permitido es ${PRECIO_MINIMO:,.0f} COP. "
                f"Precio ingresado: ${precio:,.0f} COP."
            )
>>>>>>> origin/main
