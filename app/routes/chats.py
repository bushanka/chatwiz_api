from typing import Optional

import json
from fastapi import APIRouter, Depends

from app.models.chat import ChatInfo
from app.schemas.db_schemas import Chat
from app.security.security_api import get_current_user
from app.schemas.crud import add_chat, update_chat

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)

base_message_history = json.dumps([
    ["system", "You are a helpful AI bot."],
])


@router.post('/start_new_chat', response_model=ChatInfo)
async def start_new_chat(chat_name: str,
                         user=Depends(get_current_user),
                         context_id: Optional[int] = None) -> ChatInfo:
    new_chat = Chat(name=chat_name,
                    user_id=user.id,
                    context_id=context_id,
                    message_history=base_message_history)
    new_chat_with_id = await add_chat(new_chat)
    chat_info_to_be_returned = ChatInfo(id=new_chat_with_id.id,
                                        name=new_chat_with_id.name,
                                        message_history=new_chat_with_id.message_history
                                        )
    return chat_info_to_be_returned


@router.post('/delete_chat_message_history')
async def delete_chat_message_history(chat_id: int,
                                      ):
    await update_chat(chat_id, {'message_history': base_message_history})


@router.post('/send_question')
async def send_user_question(chat_id: int, question: str):
    # message_history =
    await update_chat(chat_id, {'message_history': base_message_history})
