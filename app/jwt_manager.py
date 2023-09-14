from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
from jose import jwt
from jose import JWTError
from starlette.responses import JSONResponse
from fastapi import HTTPException

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
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Wrong access token")
    
    @classmethod
    async def decode_access(cls, token: str):
        try:
            return jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Wrong access token")

    @classmethod
    async def refresh_token(cls, refresh_token: str) -> JSONResponse:
        try:
            payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return JSONResponse(status_code=401,
                                content="Wrong format of refresh token ")
        if ('expiration' not in payload) or ('username' not in payload):
            return JSONResponse(status_code=401,
                                content="Wrong format of refresh token")
        if datetime.now().timestamp() < payload['expiration']:
            new_access_token = cls.create_access_token(payload['username'])
            return JSONResponse(status_code=200,
                                content=new_access_token)
        else:
            return JSONResponse(status_code=401,
                                content="Refresh token is expired")
