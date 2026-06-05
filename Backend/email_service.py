import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("SMTP_USER", ""),
    MAIL_PASSWORD=os.getenv("SMTP_PASSWORD", ""),
    MAIL_FROM=os.getenv("SMTP_FROM", "no-reply@vulcaria.com"),
    MAIL_FROM_NAME=os.getenv("SMTP_FROM_NAME", "Vulcaria"),
    MAIL_PORT=int(os.getenv("SMTP_PORT", 587)),
    MAIL_SERVER=os.getenv("SMTP_HOST", "smtp.azurecomm.net"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

mail = FastMail(conf)


async def enviar_email_recuperacion(email_destino: str, nombre: str, token: str):
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8000")
    link = f"{frontend_url}/reset-password?token={token}"

    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 500px; margin: auto;">
        <h2 style="color: #1a1a2e;">Recuperación de contraseña — Vulcaria</h2>
        <p>Hola <strong>{nombre}</strong>,</p>
        <p>Recibimos una solicitud para restablecer tu contraseña.
           Haz clic en el botón para crear una nueva:</p>
        <a href="{link}"
           style="display:inline-block; background:#c9a84c; color:#fff;
                  padding:12px 24px; border-radius:6px; text-decoration:none;
                  font-weight:bold; margin:16px 0;">
            Restablecer contraseña
        </a>
        <p style="color:#888; font-size:13px;">
            Este enlace expira en <strong>30 minutos</strong>.<br>
            Si no solicitaste esto, puedes ignorar este correo.
        </p>
        <hr style="border:none; border-top:1px solid #eee;">
        <p style="color:#aaa; font-size:12px;">© Vulcaria — Joyería artesanal</p>
    </div>
    """

    message = MessageSchema(
        subject="Recupera tu contraseña — Vulcaria",
        recipients=[email_destino],
        body=html,
        subtype="html",
    )

    await mail.send_message(message)
