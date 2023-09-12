from fastapi import APIRouter, status
from sqlalchemy import text
from starlette.responses import JSONResponse

from draft import asession_maker
from ..models import user

import logging

from ..schemas.crud import email_exists, add_user
from ..schemas.db_schemas import User as UserTable

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get(
    "/",
    responses={
        status.HTTP_200_OK: {
            "model": user.AuthorisedUsersInfo,
            "description": "Return all authorized users"
        },
    }
)
async def get_users() -> user.AuthorisedUsersInfo:
    # FIXME: Request to db via ORM to get users
    users = [
        user.AuthorisedUserInfo(name='Sasha', surname='Bush', email='bushanka2805@gmail.com'),
        user.AuthorisedUserInfo(name='Kirill', surname='Vasyurin', email='kirillich2912@gmail.com')
    ]
    return user.AuthorisedUsersInfo(
        users=users
    )


@router.get(
    '/{user_id}',
    responses={
        status.HTTP_200_OK: {
            'model': user.AuthorisedUserInfo,
            'description': "Return user by user_id"
        }
    }
)
async def get_user(user_id: str):
    # FIXME: Request to db via ORM to get user. Нам тут это нуэно?

    return user.AuthorisedUserInfo(
        name='Sasha',
        surname='Bush',
        email='bushanka2805@gmail.com'
    )


@router.post(
    '/register',
    responses={
        status.HTTP_200_OK: {

        }
    }
)
async def register_user(email, password, name, surname) -> JSONResponse:
    ses_maker = asession_maker
    if await email_exists(ses_maker, email):
        return JSONResponse(status_code=422, content='Email already exists')

    new_user = UserTable(
        email=email,
        password=password,
        name=name,
        surname=surname
    )
    await add_user(ses_maker, new_user)
    return JSONResponse(status_code=200, content='OK')
