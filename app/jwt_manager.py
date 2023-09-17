import os
from datetime import datetime, timedelta
from typing import Dict, Any

from dotenv import load_dotenv
from fastapi import HTTPException
from jose import JWTError
from jose import jwt
from jose.exceptions import ExpiredSignatureError

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
REFRESH_TOKEN_EXPIRE_MINUTES = timedelta(minutes=float(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")))


class JWTManager:
    @classmethod
    async def create_access_token(cls, username: str) -> str:
        data_to_encode = {'username': username,
                          'exp': datetime.utcnow() + ACCESS_TOKEN_EXPIRE_MINUTES}
        access_token = jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)
        return access_token

    @classmethod
    async def create_refresh_token(cls, username: str) -> str:
        data_to_encode = {'username': username,
                          'exp': datetime.utcnow() + REFRESH_TOKEN_EXPIRE_MINUTES}
        refresh_token = jwt.encode(data_to_encode, REFRESH_SECRET_KEY, ALGORITHM)
        return refresh_token

    @classmethod
    async def decode_refresh(cls, token: str):
        try:
            return jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Wrong access token")

    @classmethod
    async def decode_access(cls, token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature has expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Wrong access token")

    @classmethod
    async def refresh_access_token(cls, refresh_token: str):
        # Validate refresh token
        payload = await cls.decode_refresh(refresh_token)

        new_access_token = await cls.create_access_token(payload['username'])
        return new_access_token
