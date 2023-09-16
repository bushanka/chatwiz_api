import os

from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.jwt_manager import JWTManager
from app.models.user import AuthorisedUserInfo
from app.schemas.crud import get_user_info

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authorization/login",
                                     scheme_name='JWT')


async def get_current_user(access_token: str = Depends(oauth2_scheme)) -> AuthorisedUserInfo:
    payload = await JWTManager.decode_access(access_token)
    validated_payload = await JWTManager.validate_payload(payload)
    user_email = validated_payload['username']
    user = await get_user_info(user_email)
    return user
