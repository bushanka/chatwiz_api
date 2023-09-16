from pydantic import BaseModel


class SubscriptionPlanInfo(BaseModel):
    id: int
    price: float
    max_context_amount: int
    name: str
    max_context_size: int
    max_question_length: int
