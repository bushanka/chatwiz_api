import logging

from fastapi import APIRouter
from pydantic import BaseModel

from app.jwt_manager import JWTManager

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/refresh_access_token",
    tags=["refresh_access_token"],
)


class RefreshAccessTokenResponse200(BaseModel):  # мб стоит это отсюда вынести
    access_token: str
    token_type: str


@router.post('/refresh_access_token')
async def refresh_access_token(refresh_token: str) -> RefreshAccessTokenResponse200:
    new_access_token = await JWTManager.refresh_access_token(refresh_token)

    return RefreshAccessTokenResponse200(
        access_token=new_access_token,
        token_type="bearer"
    )
