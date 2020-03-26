from sqlalchemy.orm import Session
from jwcrypto import jwk

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

    db_user = models.User(email=user.email, jwk_key=key_json_str)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
