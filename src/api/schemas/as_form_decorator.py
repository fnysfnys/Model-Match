from pydantic import BaseModel
from typing import Type
from fastapi import Form
import inspect
from typing import Type

"""
Against HTTP Protocol to send files and JSON objects in the same
post method, so we use this decorator for sending model and dataset data
as form data rather than JSON.


source: https://github.com/tiangolo/fastapi/issues/2387
"""

def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls
