import json
from typing import List, Optional

from pydantic import BaseModel, Json


class ChatInfo(BaseModel):
    chat_id: int
    chat_name: str
    context_type: Optional[str] = 'pdf'  # 'pdf' | 'video' | 'site'
    creation_date: str


class ChatWithMessages(ChatInfo):
    message_history: Json


class ChatWithMessagesAndContextUrl(ChatWithMessages):
    context_url: str


class AllUserChats(BaseModel):
    chats: List[ChatInfo]


class ChatMessage(BaseModel):
    role: str
    text: str


class ChatMessages(BaseModel):
    messages: List[ChatMessage] = []

    def from_get_message_history(self, message_history):
        self.messages = [ChatMessage(role=m[0], text=m[1]) for m in json.loads(message_history)['chat']]
        return self
