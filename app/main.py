from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse

from app.security.security_api import get_current_token
from .routes import (
    authorization,
    registration,
    billing,
    context,
    refresh_access_token

)

app = FastAPI()

app.include_router(registration.router)
app.include_router(authorization.router)

app.include_router(billing.router, dependencies=[Depends(get_current_token)])
app.include_router(context.router, dependencies=[Depends(get_current_token)])
app.include_router(refresh_access_token.router, dependencies=[Depends(get_current_token)])


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
