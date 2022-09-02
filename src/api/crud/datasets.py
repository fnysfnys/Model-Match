from sqlalchemy.orm import Session

from .. import models, schemas

def create_dataset(
    db: Session,
    dataset: schemas.datasets.DatasetCreate,
    file_path: str,
    img_path: str,
    user_id: int
    ):
    db_dataset = models.Dataset(
        **dataset.dict(), 
        file_path=file_path, 
        img_path=img_path, 
        user_id=user_id
        )
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset

def get_datasets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Dataset).offset(skip).limit(limit).all()

def get_dataset_by_name(db: Session, name: str):
    return db.query(models.Dataset).filter(models.Dataset.name == name).first()

def get_dataset_by_id(db: Session, id: int):
    return db.query(models.Dataset).filter(models.Dataset.id == id).first()

def delete_dataset(db: Session, id: int):
    db.query(models.Dataset).filter(models.Dataset.id == id).delete()
    db.commit()
