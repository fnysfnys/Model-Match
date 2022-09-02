from pydantic import BaseModel
from typing import List
from .feedback import Feedback
from .as_form_decorator import as_form

"""
Pydantic schema for creating and reading models
"""

@as_form
class ModelBase(BaseModel):
    name: str
    description: str
    
    version_control: str
    release_terms: str
    outcome: str
    output: str
    output_to_trigger: str
    target_population: str
    time_of_prediction: str
    input_data_source: str
    input_data_type : str
    training_details: str
    model_type: str

class ModelCreate(ModelBase):
    pass

class Model(ModelBase):

    """
    Since ORM mode is set to True, when we read a model from the database
    we will also get a list of all the feedback for that model, based on the
    one to many relationship
    """

    id: int
    file_path: str
    img_path: str
    user_id: int
    feedback: List[Feedback] = []

    class Config:
        orm_mode = True
