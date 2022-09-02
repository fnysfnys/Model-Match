from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, index=True)
    description = Column(String)

    file_path = Column(String)
    img_path = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("User", back_populates="datasets")
