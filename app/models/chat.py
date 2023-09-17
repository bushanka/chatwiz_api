import json
from typing import List

from pydantic import BaseModel, Json


class ChatInfo(BaseModel):
    id: int
    name: str
    message_history: Json


class ChatMessage(BaseModel):
    role: str
    text: str


class ChatMessages(BaseModel):
    messages: List[ChatMessage] = []

    def from_get_message_history(self, message_history):
        print(json.loads(message_history))
        self.messages = [ChatMessage(role=m[0], text=m[1]) for m in json.loads(message_history)['chat']]
        return self
