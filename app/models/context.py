from pydantic import BaseModel


class ContextInfo(BaseModel):
    id: int
    name: str
    user_id: int
    type: str
    size: float
    path: str
