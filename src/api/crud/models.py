from sqlalchemy.orm import Session

from .. import models, schemas

def get_models(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Model).offset(skip).limit(limit).all()

def get_model_by_name(db: Session, name: str):
    return db.query(models.Model).filter(models.Model.name == name).first()

def get_model_by_id(db: Session, id: int):
    return db.query(models.Model).filter(models.Model.id == id).first()

def create_model(
    db: Session,
    model: schemas.models.ModelCreate,
    file_path: str,
    img_path: str,
    user_id: int
    ):
    db_model = models.Model(
        **model.dict(), file_path=file_path, img_path=img_path, user_id=user_id
        )
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

def delete_model(db: Session, id: int):
    db.query(models.Model).filter(models.Model.id == id).delete()
    db.commit()
