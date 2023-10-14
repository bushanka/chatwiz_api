# Схемы данных для запросов и ответов API
from pydantic import BaseModel
from typing import List


class AuthorisedUserInfo(BaseModel):
    id: int
    email: str
    name: str
    surname: str
    # hashed_password: str
    # confirmed_registration: bool
    context_ids: set = set()
    chat_ids: set = set()
    action_points_used: int
    num_of_contexts: int
    max_action_points: int
    max_number_of_contexts: int
    max_context_size: int
    max_question_length: int
    subscription_plan_id: int
