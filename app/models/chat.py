from pydantic import BaseModel, Json


class ChatInfo(BaseModel):
    id: int
    name: str
    message_history: Json
