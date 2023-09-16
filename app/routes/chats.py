from typing import Optional

from fastapi import APIRouter, Depends

from app.schemas.db_schemas import Chat
from app.security.security_api import get_current_user

router = APIRouter(
    prefix="/billing",
    tags=["billing"],
)


async def start_new_chat(user=Depends(get_current_user), context_id: Optional[int] = None):
    pass
    # new_chat = Chat(name=,
    #                 user_id=user.id,
    #                 context_id=,
    #                 )
