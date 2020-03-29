from pydantic import BaseModel


class UserMail(BaseModel):
    email: str


class UserBase(UserMail):
    pseudonym: str


class UserActivation(UserBase):
    activation_key: int


class UserLogin(UserBase):
    login_token: str


class User(UserBase):
    id: int
    is_active: bool
    jwk_key: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCount(BaseModel):
    user_count: int
