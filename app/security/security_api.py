from fastapi import HTTPException, Request
from dotenv import load_dotenv
import os


load_dotenv()
SECRET_TOKEN = os.getenv('SECRET_TOKEN')

# Функция-фабрика для создания промежуточного ПО
def auth_middleware():
    async def authenticate(request: Request, call_next):
        # Проверяем, содержится ли заголовок "Authorization" в запросе
        if "Authorization" not in request.headers:
            raise HTTPException(status_code=401, detail="Header Authorization is empty")
        
        # Получаем значение заголовка "Authorization" из запроса
        token = request.headers["Authorization"]
        
        # Проверяем, является ли токен разрешенным
        if token != SECRET_TOKEN:
            raise HTTPException(status_code=403, detail="Wrong token")
        
        # Продолжаем выполнение запроса
        response = await call_next(request)
        return response
    
    return authenticate