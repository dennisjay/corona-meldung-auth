from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    jwk_key: str


class Token(BaseModel):
    access_token: str
    token_type: str
