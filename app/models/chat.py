import json
from typing import List

from pydantic import BaseModel, Json


class ChatPdfInfo(BaseModel):
    message_history: Json
    pdf_url: str
    chat_name: str


class ChatInfo(BaseModel):
    id: int
    name: str
    message_history: Json


class ChatInfoIdName(BaseModel):
    id: int
    name: str


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
