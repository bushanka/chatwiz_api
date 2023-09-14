import logging

from fastapi import APIRouter

from app.jwt_manager import JWTManager

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/refresh_access_token",
    tags=["refresh_access_token"],
)


@router.post('/refresh_access_token')
async def refresh_access_token(refresh_token: str) -> str:
    return await JWTManager.refresh_token(refresh_token)
