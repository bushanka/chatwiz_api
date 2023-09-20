import json
from typing import Optional

from fastapi import APIRouter, Depends

from app.model_message_proccessing import get_new_message_history
from app.models.chat import ChatInfo, ChatMessages
from app.schemas.crud import (
    add_chat, 
    update_chat, 
    get_chat_message_history_by_chat_id,
    get_chat_context_name_by_chat_id
)
from app.schemas.db_schemas import Chat
from app.security.security_api import get_current_user

router = APIRouter(
    prefix="/chats",
    tags=["chats"],
)

base_message_history = json.dumps({
    "chat": [
        ["system", "You are a helpful AI bot."]
    ]
})


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
async def delete_chat_message_history(chat_id: int):
    await update_chat(chat_id, {'message_history': base_message_history})


@router.post('/send_question')
async def send_user_question(chat_id: int, question: str) -> ChatMessages:
    message_history = await get_chat_message_history_by_chat_id(chat_id)
    context_name = await get_chat_context_name_by_chat_id(chat_id)
    new_message_history = await get_new_message_history(question, message_history, context_name)
    await update_chat(chat_id, {'message_history': new_message_history})
    return ChatMessages().from_get_message_history(new_message_history)
