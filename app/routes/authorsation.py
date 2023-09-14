"""
Блок ручек по авторизации пользователя.
"""
import logging
from typing import Annotated, Any  # мб тут требуется другой

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.jwt_manager import JWTManager
from app.schemas.crud import check_credentials
from app.status_messages import StatusMessage

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/authorisation",
    tags=["authorisation"],
)


class LoginResponse200(BaseModel):  # мб стоит это отсюда вынести
    access_token: str
    refresh_token: str
    token_type: str


@router.post('/login',
             response_model=LoginResponse200)
async def login(username: str, password: str) -> JSONResponse:  # fixme понять что тут принимаем
    # username = login_data.username
    # password = login_data.password  # мб придется его тут хэшировать

    credentials_check_result = await check_credentials(username, password)
    if credentials_check_result != StatusMessage.ok.value:
        return JSONResponse(status_code=400, content=credentials_check_result)

    new_access_token = await JWTManager.create_access_token(username)
    new_refresh_token = await JWTManager.create_refresh_token(username)
    print(f'{new_access_token=}')
    return JSONResponse(status_code=200,
                        content=LoginResponse200(access_token=new_access_token,
                                                 refresh_token=new_refresh_token,
                                                 token_type="bearer").model_dump_json())  # это уберется


@router.post('/reset_password')
async def reset_password():
    pass
