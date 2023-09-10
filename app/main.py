from fastapi import FastAPI

from .routes import users, chats


app = FastAPI()


app.include_router(users.router)
app.include_router(chats.router)



# @app.get("/")
# async def root():
#     return {"message": "Hello Bigger Applications!"}