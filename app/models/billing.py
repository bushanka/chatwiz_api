from pydantic import BaseModel
from typing import List


class CreatedPayment(BaseModel):
    indepotence_key: str
    confirmation_token: str

class CancelSubscription(BaseModel):
    user_id: str
    status: str = 'cancelled'