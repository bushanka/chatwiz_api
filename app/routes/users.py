from fastapi import APIRouter, status
# from logging.config import dictConfig
from ..models import user
# from ..logs.config.logconfig import LogConfig

# import logging


# dictConfig(LogConfig().model_dump())
# logger = logging.getLogger("chatwiz")

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
async def get_users() -> user.AuthorisedUserInfo:
    # FIXME: Request to db via ORM to get users
    users = [
        user.AuthorisedUserInfo(name='Sasha', surename='Bush', email='bushanka2805@gmail.com'),
        user.AuthorisedUserInfo(name='Kirill', surename='Vasyurin', email='kirillich2912@gmail.com')
    ]
    return users