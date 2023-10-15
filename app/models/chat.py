import json
from typing import List

from pydantic import BaseModel, Json


class ChatPdfInfo(BaseModel):
    message_history: Json
    url: str  # todo переименовать
    chat_name: str
    context_type: str = 'pdf'  # 'pdf' | 'video' | 'site'


class ChatNoPdfInfo(BaseModel):
    message_history: Json
    chat_name: str
    url: str


class ChatInfo(BaseModel):
    id: int
    name: str
    message_history: Json
    context_type: str = 'pdf'  # 'pdf' | 'video' | 'site'


class ChatInfoIdName(BaseModel):
    id: int
    name: str
    context_type: str = 'pdf'  # 'pdf' | 'video' | 'site'
    creation_date: str


class AllUserChats(BaseModel):
    chats: List[ChatInfoIdName]


class ChatMessage(BaseModel):
    role: str
    text: str


class ChatMessages(BaseModel):
    messages: List[ChatMessage] = []

    def from_get_message_history(self, message_history):
        self.messages = [ChatMessage(role=m[0], text=m[1]) for m in json.loads(message_history)['chat']]
        return self
