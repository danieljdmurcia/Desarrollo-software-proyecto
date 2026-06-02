from pydantic import BaseModel, EmailStr


class RegistroSchema(BaseModel):
    nombre: str
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    nombre: str
    email: str


class RecuperarSchema(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    token: str
    nueva_password: str
