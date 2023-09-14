"""
Блок с ручками связанными с регистрацией.
"""

import logging

from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from app.schemas.crud import email_exists, add_user
from app.schemas.db_schemas import User as UserTable
from app.status_messages import StatusMessage

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/registration",
    tags=["registration"],
)


@router.post(
    '/register',
    responses={
        status.HTTP_200_OK: {

        }
    }
)
async def register_user(email: str,
                        hashed_password: str,
                        name: str,
                        surname: str) -> JSONResponse:
    if await email_exists(email):
        return JSONResponse(status_code=422, content=StatusMessage.user_exists.value)

    new_user = UserTable(
        email=email,
        password=hashed_password,
        name=name,
        surname=surname
    )

    await add_user(new_user)
    return JSONResponse(status_code=200, content=StatusMessage.new_user_created.value)
