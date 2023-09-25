import json

from fastapi import APIRouter, Depends, UploadFile
from starlette import status

from app.model_message_proccessing import get_new_message_history
from app.models.chat import ChatInfo, ChatMessages, AllUserChats, ChatPdfInfo
from app.models.user import AuthorisedUserInfo
from app.routes.context import create_upload_file
from app.schemas.crud import (
    add_chat,
    update_chat,
    get_chat_message_history_by_chat_id,
    get_chat_context_name_by_chat_id,
    get_chatinfo_by_chat_id, delete_chat
)
from app.schemas.crud import get_user_chats_from_db
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
async def start_new_chat(
        chat_name: str,
        file: UploadFile,
        user=Depends(get_current_user)
) -> ChatInfo:
    context_id = await create_upload_file(file, user)
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


@router.post('/change_chat_name/{chat_id}')
async def change_chat_name(chat_id: int, new_name):  # todo
    await update_chat(chat_id, {'name': new_name})


@router.delete('/delete_chat/{chat_id}',
               responses={
                   status.HTTP_200_OK: {
                       "description": "Chat has been deleted"
                   },
               }
               )
async def delete_chat_handle(chat_id: int):
    await delete_chat(chat_id)
    return 'ok' # todo


@router.post(
    "/get_chats/",
    responses={
        status.HTTP_200_OK: {
            "description": "Return all user chats"
        },
    }
)
async def get_user_chats(user: AuthorisedUserInfo = Depends(get_current_user)) -> AllUserChats:
    user_chats = await get_user_chats_from_db(user.id)
    return user_chats


@router.post(
    "/get_chatinfo/",
    responses={
        status.HTTP_200_OK: {
            "description": "Return info about user chat (pdf url and history)"
        },
    }
)
async def get_user_chats(chat_id: int, user: AuthorisedUserInfo = Depends(get_current_user)) -> ChatPdfInfo:
    user_chatinfo = await get_chatinfo_by_chat_id(chat_id)
    return user_chatinfo
