from pydantic import BaseModel

"""
Pydantic schema for creating and reading feedback
"""

class FeedbackBase(BaseModel):
    feedback_type: str
    feedback_catagory: str
    feedback: str

class FeedbackCreate(FeedbackBase):
    pass

class Feedback(FeedbackBase):
    id: int
    model_id: int
    user_id: int

    class Config:
        orm_mode = True
