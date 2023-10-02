from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.routes import (
    authorization,
    registration,
    billing,
    context,
    refresh_access_token,
    chats,
    password_change,
    delete_account,
    user_information,
    feedback

)
from app.schemas.crud import apgvector_instance
from app.security.security_api import get_current_user

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(registration.router)
app.include_router(authorization.router)
app.include_router(refresh_access_token.router)

app.include_router(billing.router, dependencies=[Depends(get_current_user)])
app.include_router(context.router, dependencies=[Depends(get_current_user)])
app.include_router(chats.router, dependencies=[Depends(get_current_user)])
app.include_router(password_change.router, dependencies=[Depends(get_current_user)])
app.include_router(delete_account.router, dependencies=[Depends(get_current_user)])
app.include_router(user_information.router, dependencies=[Depends(get_current_user)])
app.include_router(feedback.router, dependencies=[Depends(get_current_user)])


@app.on_event("startup")
async def startup():
    await apgvector_instance.connect()
    # gunicorn_logger = logging.getLogger('gunicorn.error')
    # logger = logging.getLogger("uvicorn")
    # handler = logging.handlers.RotatingFileHandler("api.log", mode="a", maxBytes=100 * 1024, backupCount=3)
    # handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    # logger.addHandler(handler)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
