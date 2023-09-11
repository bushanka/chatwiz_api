from pydantic import BaseModel
from typing import List


class CreatedPayment(BaseModel):
    indepotence_key: str
    confirmation_token: str