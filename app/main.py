from fastapi import FastAPI

from .routes import (
    users,
    chats,
    billing,
    context
)

app = FastAPI()

app.include_router(users.router)
app.include_router(billing.router)
app.include_router(context.router)

# @app.get("/")
# async def root():
#     return {"message": "Hello Bigger Applications!"}
