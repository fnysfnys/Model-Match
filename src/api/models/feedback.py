from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base

class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    feedback_type = Column(String)
    feedback_catagory = Column(String)

    feedback = Column(String)

    model_id = Column(Integer, ForeignKey("models.id", ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("User", back_populates="feedback")
    models = relationship("Model", back_populates="feedback")
