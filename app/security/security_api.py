import os

from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.jwt_manager import JWTManager

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authorization/login",
                                     scheme_name='JWT')


# Зависимость для получения текущего токена
async def get_current_token(access_token: str = Depends(oauth2_scheme)):
    payload = await JWTManager.decode_access(access_token)
    return await JWTManager.validate_payload(payload)
