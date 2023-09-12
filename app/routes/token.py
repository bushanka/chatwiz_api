from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
from typing import Annotated
from hashlib import sha256
from jose import jwt

import os
import logging

load_dotenv()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_HASHED_PASSWORD = os.getenv("ADMIN_HASHED_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/token",
    tags=["token"],
)


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