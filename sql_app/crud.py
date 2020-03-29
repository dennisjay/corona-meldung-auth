from random import randint
from sqlalchemy.orm import Session
from jwcrypto import jwk
from datetime import datetime
import uuid

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserBase):
    key = jwk.JWK.generate(kty='oct', size=256)
    key_json_str = key.export()
    activation_key = randint(1000, 9999)
    pseudonym = str(uuid.uuid4())

    db_user = models.User(email=user.email, jwk_key=key_json_str, activation_key=activation_key, pseudonym=pseudonym)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def activate_user(db: Session, db_user: models.User):
    db_user.is_active = True
    db_user.activation_key = 0
    db.commit()
    db.refresh(db_user)
    return db_user


def prepare_login(db: Session, db_user: models.User, login_token: str):
    db_user.login_token = login_token
    db_user.timestamp_log_in_token = datetime.now()
    db.commit()
    db.refresh(db_user)
    return db_user


def login_user(db: Session, db_user: models.User):
    db_user.logged_in = True
    db_user.login_token = ''
    db_user.timestamp_log_in_token = datetime.min
    db.commit()
    db.refresh(db_user)
    return db_user


def count_users(db: Session):
    return db.query(models.User).count()
