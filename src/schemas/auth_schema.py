from datetime import timedelta
from pydantic import BaseModel


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str


class RegisterResponseSchema(BaseModel):
    message: str


class LoginSchema(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
