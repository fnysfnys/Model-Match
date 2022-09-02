import os
from typing import List
from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_current_user
from .. import crud, schemas, permissions

router = APIRouter(
    prefix="/api/datasets",
    tags=["datasets"]
)

@router.post("/upload", response_model=schemas.datasets.Dataset)
def create_dataset(
    dataset: schemas.datasets.DatasetBase = Depends(
        schemas.datasets.DatasetBase.as_form
        ),
    file: UploadFile = File(...),
    display_img: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """
    Takes in dataset metadata defined by the DatasetBase model
    (name, description, ...) aswell as the dataset itself.

    Validates the uploader has the valid permissions,
    and checks the given name is unique.

    Writes the dataset to src/data/datasets as a zip and writes a record of
    the dataset to the database, this will include the metadata, filepath,
    and the user_id of the user who uploaded it.
    """

    if current_user.permissions == permissions.READ:
        raise HTTPException(status_code=401, detail="Unauthorised")

    db_dataset = crud.datasets.get_dataset_by_name(db, name=dataset.name)
    if db_dataset:
        raise HTTPException(status_code=400, detail="Name already registered")

    file_path = f'{os.getcwd()}/data/datasets/{dataset.name.replace(" ", "_").lower()}.zip'
    
    with open(file_path,'wb+') as f:
        f.write(file.file.read())
        f.close()

    img_path = f'{os.getcwd()}/data/images/datasets/{dataset.name.replace(" ", "_").lower()}'

    with open(img_path,'wb+') as f:
        f.write(display_img.file.read())
        f.close()

    return crud.datasets.create_dataset(
        db=db,
        dataset=dataset,
        file_path=file_path,
        img_path=img_path,
        user_id=current_user.id
        )

@router.get("/{dataset_id}", response_model=schemas.datasets.Dataset)
def read_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """returns a dataset record in the database by it's id"""

    db_dataset = crud.datasets.get_dataset_by_id(db=db, id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return db_dataset

@router.get("/", response_model=List[schemas.datasets.Dataset])
def read_datasets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """returns all datasets in the database"""

    datasets = crud.datasets.get_datasets(db, skip=skip, limit=limit)
    return datasets

@router.get("/{dataset_id}/download")
def download_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """returns the zip file of the dataset with the given id"""

    db_dataset = crud.datasets.get_dataset_by_id(db, id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    file_path = db_dataset.file_path

    return FileResponse(file_path)

@router.get("/{dataset_id}/display-image")
def read_display_image(
    dataset_id: int,
    db: Session = Depends(get_db),
    # current_user: schemas.users.User = Depends(get_current_user)
    ):

    """Returns the model display image for the given ID"""

    db_dataset = crud.datasets.get_dataset_by_id(db=db, id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return FileResponse(db_dataset.img_path)

@router.delete("/{dataset_id}/delete")
def delete_dataset(
    dataset_id: str,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """
    Verifies the user requesting the delete is the one who uploaded the
    dataset, If so, deletes the record of the dataset in the database and the
    corresponding zip file in src/data/datasets.
    """

    db_dataset = crud.datasets.get_dataset_by_id(db, id=dataset_id)
    if db_dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")
    if db_dataset.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorised")
    os.remove(db_dataset.file_path)
    os.remove(db_dataset.img_path)
    crud.datasets.delete_dataset(db=db, id=dataset_id)
    return {"ok": True}
