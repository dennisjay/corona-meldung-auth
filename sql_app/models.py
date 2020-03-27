from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=False)
    activation_key = Column(Integer)
    logged_in = Column(Boolean, default=False)
    login_token = Column(String(50), default='')
    timestamp_log_in_token = Column(DateTime, default=datetime.now())
    jwk_key = Column(Text)
