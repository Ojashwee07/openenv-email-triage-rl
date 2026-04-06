from pydantic import BaseModel

class Observation(BaseModel):
    email_text: str
    sender: str
    urgency: int
    step_count: int

class Action(BaseModel):
    action_type: str

class Reward(BaseModel):
    value: float
