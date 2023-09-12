from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from app.security.security_api import auth_middleware

from .routes import (
    users,
    chats,
    billing,
    context
)

app = FastAPI()


app.middleware("http")(auth_middleware)

app.include_router(users.router)
app.include_router(billing.router)
app.include_router(context.router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
