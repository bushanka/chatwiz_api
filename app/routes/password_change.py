import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from app.models.user import AuthorisedUserInfo
from app.password_hashing import password_encoder
from app.schemas.crud import get_user_hashed_password, update_user
from app.security.security_api import get_current_user
from app.status_messages import StatusMessage

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/password_change",
    tags=["password_change"],
)


@router.post('/')
async def reset_password(old_password: str,
                         new_password: str,
                         user: AuthorisedUserInfo = Depends(get_current_user),
                         ):
    user_cur_password = await get_user_hashed_password(user.email)
    hashed_password = await password_encoder(old_password)
    print(user_cur_password, hashed_password)
    if user_cur_password == hashed_password:
        new_hashed_password = await password_encoder(new_password)
        await update_user(user.email, {'hashed_password': new_hashed_password})
        return JSONResponse(content=StatusMessage.password_changed.value, status_code=200)
    else:
        raise HTTPException(status_code=400, detail=StatusMessage.wrong_password.value)
