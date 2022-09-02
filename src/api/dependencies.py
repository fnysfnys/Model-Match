from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from . import crud
from . import schemas
from sqlalchemy.orm import Session
from .database import SessionLocal
from .auth import oauth2_scheme, SECRET_KEY, ALGORITHM

"""
Defines the dependencies for the endpoints, the end points depend on a
database connection (get_db) and auth with a JWT (get_current_user)

Auth handled in auth.py
"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
    ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.tokens.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.users.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

