import logging

from fastapi import APIRouter, status, Depends

from app.models.user import AuthorisedUserInfo
from app.security.security_api import get_current_user

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/user_information",
    tags=["user_information"],
)


@router.get(
    '/',
    responses={
        status.HTTP_200_OK: {

        }
    }
)
async def get_user_info_for_display(user: AuthorisedUserInfo = Depends(get_current_user)):
    return user
