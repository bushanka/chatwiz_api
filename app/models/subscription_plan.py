from pydantic import BaseModel, ConfigDict


class SubscriptionPlanInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    price: float
    max_context_amount: int
    name: str
    max_context_size: int
    max_question_length: int
    max_action_points: int
