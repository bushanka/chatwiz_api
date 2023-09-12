from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from app.security.security_api import get_current_token

from .routes import (
    users,
    chats,
    billing,
    context,
    token
)

app = FastAPI()

# Защищенные роутеры с помощью зависимости get_current_token
app.include_router(users.router, dependencies=[Depends(get_current_token)])
app.include_router(billing.router, dependencies=[Depends(get_current_token)])
app.include_router(context.router, dependencies=[Depends(get_current_token)])

# Незащищенный роутер для получения токена
app.include_router(token.router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
