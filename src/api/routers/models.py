import os
from typing import List
from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_current_user
from .. import crud, permissions, model_gen, model_download, schemas
from starlette.background import BackgroundTasks

router = APIRouter(
    prefix="/api/models",
    tags=["models"]
)

@router.post("/upload", response_model=schemas.models.Model)
def create_model(
    model: schemas.models.ModelBase = Depends(
        schemas.models.ModelBase.as_form
        ),
    requirements: UploadFile = File(...),
    source_code: UploadFile = File(...),
    pickle: UploadFile = File(...),
    config: UploadFile = File(...),
    display_img: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """
    Takes in the model metadata (name, description, VC, etc...),
    the source code as a zip, the requirements as a txt,
    and a pickle of the trained model.


    Authenticates the user has the correct permissions for writing data,
    and that the model name is unique. Passes data to model_gen where the 
    docker image containing the model is created and saved. 
    model_gen returns a file_path of the model tar file,
    which is then written to the database.
    """

    if current_user.permissions == permissions.READ:
        raise HTTPException(status_code=401, detail="Unauthorised")

    db_model = crud.models.get_model_by_name(db, name=model.name)
    if db_model:
        raise HTTPException(status_code=400, detail="Name already registered")

    file_path = model_gen.create_model(
        model,
        requirements,
        source_code,
        pickle,
        config
        )

    img_path = f'{os.getcwd()}/data/images/models/{model.name.replace(" ", "_").lower()}'

    with open(img_path,'wb+') as f:
        f.write(display_img.file.read())
        f.close()

    return crud.models.create_model(
        db=db,
        model=model,
        file_path=file_path,
        img_path=img_path,
        user_id=current_user.id
        )

@router.get("/{model_id}", response_model=schemas.models.Model)
def read_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """Returns model record in database by id"""

    db_model = crud.models.get_model_by_id(db=db, id=model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return db_model

@router.get("/", response_model=List[schemas.models.Model])
def read_models(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """Returns all model records in the database"""
    
    models = crud.models.get_models(db, skip=skip, limit=limit)
    return models


def remove_file(file_path: str) -> None:

    """
    Added as a background task so the temporary file can be deleted after
    the response has been sent.

    source: https://stackoverflow.com/questions/64716495/how-to-delete-the-file-after-a-return-fileresponsefile-path
    """

    os.remove(file_path)

@router.get("/{model_id}/download/")
def download_model(
    model_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """
    Takes in a model_id and returns the .tar file of the corresponding model.
    If the user has not downloaded this model before,
    keep a record of download for submitting feedback.
    """

    db_model = crud.models.get_model_by_id(db, id=model_id)

    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    file_path = db_model.file_path

    db_download = crud.downloads.get_download(
        db=db,
        model_id=db_model.id,
        user_id=current_user.id
        )

    if db_download is None:
        crud.downloads.create_download(
            db=db,
            model_id=db_model.id,
            user_id=current_user.id
            )

    file_path = model_download.generate_download(db_model)
    background_tasks.add_task(remove_file, file_path)
    return FileResponse(file_path)

@router.get("/{model_id}/display-image")
def read_display_image(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """Returns the model display image for the given ID"""

    db_model = crud.models.get_model_by_id(db=db, id=model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return FileResponse(db_model.img_path)

@router.delete("/{model_id}/delete")
def delete_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """
    Verifies the user requesting the delete is the one who uploaded the model,
    If so, deletes the record of the model in the database and the corresponding
    tar file in src/models
    """

    db_model = crud.models.get_model_by_id(db, id=model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    if db_model.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorised")
    os.remove(db_model.file_path)
    os.remove(db_model.img_path)
    crud.models.delete_model(db=db, id=model_id)
    return {"ok": True}
