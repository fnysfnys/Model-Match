from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base

class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, index=True)
    description = Column(String)
    
    # parameters defined by carefulai
    version_control = Column(String)
    release_terms = Column(String)
    outcome = Column(String)
    output = Column(String)
    output_to_trigger = Column(String)
    target_population = Column(String)
    time_of_prediction = Column(String)
    input_data_source = Column(String)
    input_data_type = Column(String)
    training_details = Column(String)
    model_type  = Column(String)

    file_path = Column(String)
    img_path = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    users = relationship("User", back_populates="models")
    feedback = relationship(
        "Feedback",
        back_populates="models",
        passive_deletes=True
        )
    downloads = relationship(
        "Download",
        back_populates="models",
        passive_deletes=True
        )
