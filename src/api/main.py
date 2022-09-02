import os
from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .routers import datasets, feedback, models, users

from .dependencies import get_db
from .auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token
from . import schemas

"""
The main file which ties everything together.

We create our FastAPI class and include our routers.
"""

app = FastAPI()

app.include_router(users.router)
app.include_router(datasets.router)
app.include_router(models.router)
app.include_router(feedback.router)

@app.post("/api/token", response_model=schemas.tokens.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):

    """
    Authenticates users and returns an access token as a JWT.

    Authentication handled with OAuth2 with Password (and hashing),
    Bearer with JWT tokens.

    reference: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    """
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
