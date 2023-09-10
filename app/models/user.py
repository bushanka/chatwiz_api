# Схемы данных для запросов и ответов API
from pydantic import BaseModel
from typing import List


class AuthorisedUserInfo(BaseModel):
    name: str
    surname: str
    email: str


class AuthorisedUsersInfo(BaseModel):
    users: List[AuthorisedUserInfo]


class AuthorisedUserToken(BaseModel):
    authorised_user_token: str