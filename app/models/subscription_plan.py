from pydantic import BaseModel


class SubscriptionPlanInfo(BaseModel):
    id: int
    price: float
    max_content_amount: int
    name: str
    max_content_size: int
    max_question_length: int
