from typing import Optional
from pydantic import BaseModel

"""
Pydantic Models that will be used in the token endpoint for the response.

Source: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
"""

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
