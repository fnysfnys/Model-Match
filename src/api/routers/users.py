from typing import List
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_current_user
from .. import crud, schemas

from .. import permissions

router = APIRouter(
    prefix="/api/users",
    tags=["users"]
)

@router.post("/create", response_model=schemas.users.User)
def create_user(
    user: schemas.users.UserCreate,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """
    Takes in new user data, verifies the email and username are unique,
    then creates a record of the user.

    Since this is a closed system, only users with create_user permissions
    can create a user.
    """

    if current_user.permissions != permissions.READ_WRITE_CREATE_USERS:
        raise HTTPException(status_code=401, detail=f"Unauthorised")
    
    db_user = crud.users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.users.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
            )
    return crud.users.create_user(db=db, user=user)

@router.post("/change-password", response_model=schemas.users.User)
def change_password(
    new_password: schemas.users.NewPassword,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    if new_password.password != new_password.confirmation:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    return crud.users.update_password(
        db,
        current_user=current_user,
        new_password=new_password
        )
    

@router.get("/me", response_model=schemas.users.User)
async def read_users_me(
    current_user: schemas.users.User = Depends(get_current_user)
    ):
    """Returns the current user given a JWT."""
    return current_user

@router.get("/{username}/", response_model=schemas.users.User)
def read_user(
    username: str,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """
    Returns the user details of the user corresponding to the given username,
    Including their datasets, models, feedback and downloads.
    
    (see schema.user.User)
    """

    db_user = crud.users.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/my-downloads",
response_model=List[schemas.downloads.ModelDownload]
)
def read_downloads(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """
    Returns the list of all models the current user has downloaded
    as a list of ModelDownload objects (id and name of model)

    (see schema.download.ModelDownload)
    """

    downloads = crud.downloads.get_downloads(
        user_id=current_user.id,
        db=db, skip=skip,
        limit=limit
        )

    model_downloads = []
    for download in downloads:
        db_model = crud.models.get_model_by_id(db, download.model_id)
        model_download = schemas.downloads.ModelDownload(
            id=db_model.id,
            name=db_model.name
            )
        model_downloads.append(model_download)
    return model_downloads
