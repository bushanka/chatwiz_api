from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from jose import jwt, JWTError
import os


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token/admin")


# Функция для проверки и декодирования токена
async def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    # FIXME: separetly handle expiration error and wrong token error if possible
    except JWTError:
        raise HTTPException(status_code=401, detail="Wrong token")

# Зависимость для получения текущего токена
async def get_current_token(token: str = Depends(oauth2_scheme)):
    payload = await decode_token(token)
    return payload