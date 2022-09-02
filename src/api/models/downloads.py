from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base

class Download(Base):
    __tablename__ = "downloads"

    id = Column(Integer, primary_key=True, index=True)
    
    model_id = Column(Integer, ForeignKey("models.id", ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", back_populates="downloads")
    models = relationship("Model", back_populates="downloads")
