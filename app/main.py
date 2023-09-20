from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from app.schemas.crud import apgvector_instance
# from fastapi.middleware.cors import CORSMiddleware

from app.security.security_api import get_current_user
from app.routes import (
    authorization,
    registration,
    billing,
    context,
    refresh_access_token,
    chats

)

app = FastAPI()
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
app.include_router(registration.router)
app.include_router(authorization.router)
app.include_router(refresh_access_token.router)

app.include_router(billing.router, dependencies=[Depends(get_current_user)])
app.include_router(context.router, dependencies=[Depends(get_current_user)])
app.include_router(chats.router, dependencies=[Depends(get_current_user)])


@app.on_event("startup")
async def startup():
    await apgvector_instance.connect()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")