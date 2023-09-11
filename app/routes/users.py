from fastapi import APIRouter, status
from ..models import user

import logging


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
    # FIXME: Request to db via ORM to get user

    return user.AuthorisedUserInfo(
        name='Sasha', 
        surname='Bush', 
        email='bushanka2805@gmail.com'
    )