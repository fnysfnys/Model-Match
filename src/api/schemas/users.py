from pydantic import BaseModel

from typing import List, Optional
from .datasets import Dataset
from .models import Model
from .feedback import Feedback
from .downloads import Download

"""
Pydantic model for user, here we can see password is in UserCreate,
this is so that the password will not be sent by the API when reading a user.
"""

class UserBase(BaseModel):
    email: str
    username: str
    permissions: int

class UserCreate(UserBase):
    password: str

class User(UserBase):

    """
    Since ORM is set to true, when we read a user from the database, 
    we can also get the data of all of the datasets, models and feedback the
    user has uploaded, aswell as their downloads.
    """
    
    id: int
    datasets: List[Dataset] = []
    models: List[Model] = []
    feedback: List[Feedback] = []
    downloads: List[Download] = []

    class Config:
        orm_mode = True

class NewPassword(BaseModel):
    password: str
    confirmation: str