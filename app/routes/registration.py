"""
Блок с ручками связанными с регистрацией.
"""

import logging

from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.jwt_manager import JWTManager
from app.password_hashing import password_encoder
from app.schemas.crud import email_exists, add_user
from app.schemas.db_schemas import User as UserTable
from app.status_messages import StatusMessage

from email_validator import validate_email, EmailNotValidError

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/registration",
    tags=["registration"],
)


class AuthResponse200(BaseModel):  # мб стоит это отсюда вынести
    status: str
    access_token: str
    refresh_token: str
    user_id: int


@router.post(
    '/register',
    responses={
        status.HTTP_200_OK: {

        }
    }
)
async def register_user(email: str,
                        password: str,
                        name: str = "default_name",
                        surname: str = "default_surname"):
    if await email_exists(email):
        raise HTTPException(status_code=422, detail=StatusMessage.user_exists.value)
    if len(password) <= 6:
        raise HTTPException(status_code=422, detail=StatusMessage.password_too_short.value)
    try:
        email = validate_email(email).ascii_email
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=str(e))
    new_user = UserTable(
        email=email,
        hashed_password=await password_encoder(password),
        name=name,
        surname=surname
    )

    new_access_token = await JWTManager.create_access_token(email)
    new_refresh_token = await JWTManager.create_refresh_token(email)

    await add_user(new_user)

    return AuthResponse200(
        status=StatusMessage.new_user_created.value,
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        user_id=new_user.id
    )
    # return JSONResponse(status_code=200, content=StatusMessage.new_user_created.value)
