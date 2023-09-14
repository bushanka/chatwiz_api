import os
from datetime import datetime, timedelta
from typing import Dict, Any

from dotenv import load_dotenv
from fastapi import HTTPException
from jose import JWTError
from jose import jwt

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
                          'expiration': (datetime.now() + ACCESS_TOKEN_EXPIRE_MINUTES).timestamp()}
        access_token = jwt.encode(data_to_encode, SECRET_KEY, ALGORITHM)
        return access_token

    @classmethod
    async def create_refresh_token(cls, username: str) -> str:
        data_to_encode = {'username': username,
                          'expiration': (datetime.now() + REFRESH_TOKEN_EXPIRE_MINUTES).timestamp()}
        refresh_token = jwt.encode(data_to_encode, REFRESH_SECRET_KEY, ALGORITHM)
        return refresh_token

    @classmethod
    async def decode_refresh(cls, token: str):
        try:
            return jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Wrong access token")

    @classmethod
    async def decode_access(cls, token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Wrong access token")

    @classmethod
    async def validate_payload(cls, token_payload: Dict[str, Any]):
        if ('expiration' not in token_payload) or ('username' not in token_payload):
            raise HTTPException(status_code=401,
                                detail="Wrong format of refresh token")
        if datetime.now().timestamp() > token_payload['expiration']:
            print(f'{datetime.now().timestamp() > token_payload["expiration"]=}')
            raise HTTPException(status_code=401,
                                detail="Refresh token is expired")
        return token_payload

    @classmethod
    async def refresh_token(cls, refresh_token: str):
        payload = await cls.decode_refresh(refresh_token)
        valid_payload = cls.validate_payload(payload)
        return valid_payload
