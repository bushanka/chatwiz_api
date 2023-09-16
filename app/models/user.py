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
    num_of_requests_used: int
    num_of_contexts: int
    subscription_plan_id: int

# class AuthorisedUsersInfo(BaseModel):
#     users: List[AuthorisedUserInfo]


# class AuthorisedUserToken(BaseModel):
#     authorised_user_token: str
