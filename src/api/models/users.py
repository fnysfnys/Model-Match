from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    permissions = Column(Integer)

    datasets = relationship("Dataset", back_populates="users")
    models = relationship("Model", back_populates="users")
    feedback = relationship("Feedback", back_populates="users")
    downloads = relationship("Download", back_populates="users")
