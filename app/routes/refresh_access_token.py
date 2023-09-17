import logging

from fastapi import APIRouter

from app.jwt_manager import JWTManager
from pydantic import BaseModel


logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/refresh_access_token",
    tags=["refresh_access_token"],
)

class RefreshTokensResponse200(BaseModel):  # мб стоит это отсюда вынести
    access_token: str
    refresh_token: str
    token_type: str


@router.post('/refresh_access_token')
async def refresh_access_token(refresh_token: str, username: str) -> RefreshTokensResponse200:
    new_tokens = await JWTManager.refresh_tokens(refresh_token, username)

    return RefreshTokensResponse200(access_token=new_tokens['access_token'],
                            refresh_token=new_tokens['refresh_token'],
                            token_type="bearer")
