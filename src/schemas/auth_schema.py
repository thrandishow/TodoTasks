from pydantic import BaseModel


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str


class RegisterResponseSchema(BaseModel):
    message: str


class LoginSchema(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
