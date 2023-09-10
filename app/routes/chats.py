from fastapi import APIRouter, status
from ..models import user



router = APIRouter(
    prefix="/chats",
    tags=["chats"],
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
    # Request to db via ORM from models
    users = [
        user.AuthorisedUserInfo(name='Sasha', surename='Bush', email='bushanka2805@gmail.com'),
        user.AuthorisedUserInfo(name='Kirill', surename='Vasyurin', email='kirillich2912@gmail.com')
    ]
    return users