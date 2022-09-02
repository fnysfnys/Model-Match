from pydantic import BaseModel

"""
Pydantic schema for creating and reading downloads
"""

class DownloadBase(BaseModel):
    pass

class DownloadCreate(DownloadBase):
    pass

class Download(DownloadBase):
    id: int
    model_id: int
    user_id: int

    class Config:
        orm_mode = True

class ModelDownload(BaseModel):

    """
    Used to display the id and name of the model downloaded
    """

    id: int
    name: str
