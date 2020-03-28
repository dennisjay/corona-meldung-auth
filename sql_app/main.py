from datetime import timedelta, datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from sql_app.auth import get_current_active_user, authenticate_user, create_access_token, create_login_token
from . import crud, models, schemas, mail_sender
from .database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://corona-meldung.s3-website.eu-central-1.amazonaws.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register", response_model=schemas.UserActivation)
def register_user(user: schemas.UserBase, db: Session = Depends(get_db)):

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.create_user(db=db, user=user)

    # Sent Email with activation key to use in confirm_user()
    activation_key = db_user.activation_key
    mail_sender.send_register_mail(user.email, activation_key)

    return schemas.UserActivation(email=db_user.email, activation_key=db_user.activation_key)


@app.post("/confirm", response_model=schemas.User)
def confirm_user(user: schemas.UserActivation, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    # Check if user exists or has been activated before
    if not db_user:
        raise HTTPException(status_code=400, detail="Email not registered")
    elif db_user.is_active:
        raise HTTPException(status_code=400, detail="User already activated")

    # Check if activation key is valid
    if not user.activation_key == db_user.activation_key:
        raise HTTPException(status_code=400, detail="Activation key not valid")

    # Check if activation worked
    if crud.activate_user(db=db, db_user=db_user):
        return schemas.User(id=db_user.id, email=db_user.email, is_active=db_user.is_active, jwk_key=db_user.jwk_key)
    else:
        raise HTTPException(status_code=400, detail="Could not activate user")


@app.post("/login", response_model=schemas.UserBase)
def login_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email not registered")

    # Set login token in db and sent via Email
    login_token = create_login_token()
    crud.prepare_login(db=db, db_user=db_user, login_token=login_token)
    mail_sender.send_login_mail(user.email, login_token)

    return schemas.UserBase(email=db_user.email)


@app.post("confirm_login", response_model=schemas.User)
def confirm_login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)

    # Check if user exists and has been activated before
    if not db_user:
        raise HTTPException(status_code=400, detail="Email not registered")
    elif not db_user.is_active:
        raise HTTPException(status_code=400, detail="User not yet activated")

    # Check if login token is valid and not expired
    if not user.login_token == '' or not user.login_token == db_user.login_token:
        raise HTTPException(status_code=400, detail="Login token not valid")
    elif datetime.now() - db_user.timestamp_log_in_token > timedelta(minutes=15):
        raise HTTPException(status_code=400, detail="Login token has expired")

    # Check if login worked
    if crud.login_user(db=db, db_user=db_user):
        return schemas.User(id=db_user.id, email=db_user.email, is_active=db_user.is_active, jwk_key=db_user.jwk_key)
    else:
        raise HTTPException(status_code=400, detail="Could not activate user")


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.create_user(db=db, user=user)
    return schemas.User(id=db_user.id, email=db_user.email, is_active=db_user.is_active, jwk_key=db_user.jwk_key)


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return schemas.User(id=current_user.id, email=current_user.email, is_active=current_user.is_active, jwk_key=current_user.jwk_key)


