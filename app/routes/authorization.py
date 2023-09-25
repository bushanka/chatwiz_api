"""
Блок ручек по авторизации пользователя.
"""
import logging
from typing import Annotated  # мб тут требуется другой

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.jwt_manager import JWTManager
from app.schemas.crud import check_credentials
from app.status_messages import StatusMessage

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/authorization",
    tags=["authorization"],
)


class LoginResponse200(BaseModel):  # мб стоит это отсюда вынести
    access_token: str
    refresh_token: str
    token_type: str


@router.post('/login',
             response_model=LoginResponse200)
async def login(    
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password  # мб придется его тут хэшировать

    credentials_check_result = await check_credentials(username, password)
    if credentials_check_result != StatusMessage.ok.value:
        raise HTTPException(status_code=400, detail=credentials_check_result)

    new_access_token = await JWTManager.create_access_token(username)
    new_refresh_token = await JWTManager.create_refresh_token(username)
    return LoginResponse200(access_token=new_access_token,
                            refresh_token=new_refresh_token,
                            token_type="bearer")

# @router.post('/reset_password')
# async def reset_password():
#     pass
