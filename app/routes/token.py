from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Union
from dotenv import load_dotenv
from typing import Annotated
from hashlib import sha256
from jose import jwt
from datetime import timedelta

import datetime
import os
import logging


load_dotenv()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_HASHED_PASSWORD = os.getenv("ADMIN_HASHED_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/token",
    tags=["token"],
)


def create_user_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/admin/")
async def admin_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    admin_username = form_data.username
    admin_password = form_data.password

    if admin_username != ADMIN_USERNAME:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if ADMIN_HASHED_PASSWORD != sha256(admin_password.encode('utf-8')).hexdigest():
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    token = jwt.encode({"username": admin_username}, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}


@router.post('/user')
async def user_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password

    # FIXME: Check username and hashed password

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_user_access_token(
        data={"username": username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}