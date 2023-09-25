import json
from typing import List

from pydantic import BaseModel, Json


class ChatPdfInfo(BaseModel):
    message_history: Json
    pdf_url: str


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
        # print(f'1:\n\n{message_history}\n\n')
        # print(f'2:\n\n{json.loads(message_history)}\n\n')
        self.messages = [ChatMessage(role=m[0], text=m[1]) for m in json.loads(message_history)['chat']]
        return self
