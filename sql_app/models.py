from sqlalchemy import Boolean, Column, Integer, String, Text

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=False)
    activation_key = Column(Integer)
    jwk_key = Column(Text)
