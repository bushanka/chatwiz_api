from pydantic import BaseModel
from typing import List


class ContextInfo(BaseModel):
    id: int
    name: str
    user_id: int
    type: str
    size: float
    path: str


class UserContextsInfo(BaseModel):
    contexts: List[ContextInfo]