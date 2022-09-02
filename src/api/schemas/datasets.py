from pydantic import BaseModel

from .as_form_decorator import as_form

"""
Pydantic models/schema for datasets.

We use DatasetBase to pass in dataset metadata like its name and discription
when creating a dataset.

Before creating an item we don't know its id, filepath and user_id of the 
uploader, but when we read it from the database we will. So we then have our
Dataset schema, which inherits the base model.
"""

@as_form
class DatasetBase(BaseModel):
    name: str
    description: str

class DatasetCreate(DatasetBase):
    pass

class Dataset(DatasetBase):
    id: int
    file_path: str
    img_path: str
    user_id: int

    class Config:
        orm_mode = True
