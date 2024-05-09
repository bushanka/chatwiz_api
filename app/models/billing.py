from pydantic import BaseModel
from typing import List


class CreatedPayment(BaseModel):
    indepotence_key: str
    redirect_url: str

class CancelSubscription(BaseModel):
    user_id: str
    status: str = 'cancelled'