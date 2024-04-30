import asyncio
import logging

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from app.models.user import AuthorisedUserInfo
from app.schemas.crud import delete_chat, delete_user, delete_context
from app.security.security_api import get_current_user
from app.status_messages import StatusMessage

logger = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/delete_account",
    tags=["delete_account"],
)


@router.delete(
    "/",
    responses={
        status.HTTP_200_OK: {
            "description": "Return given context"
        },
    }
)
async def delete_account(user: AuthorisedUserInfo = Depends(get_current_user)) -> JSONResponse:
    list_of_coroutines = [delete_chat(chat_id) for chat_id in user.chat_ids]
    list_of_coroutines += [delete_context(context_id) for context_id in user.context_ids]
    list_of_coroutines += [delete_user(user.email)]
    await asyncio.gather(*list_of_coroutines)
    return JSONResponse(status_code=200, content=StatusMessage.user_deleted.value)
