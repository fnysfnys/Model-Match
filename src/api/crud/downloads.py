from statistics import mode
from sqlalchemy.orm import Session

from .. import models

def create_download(db: Session, model_id: int, user_id: int):
    db_download = models.Download(model_id=model_id, user_id=user_id)
    db.add(db_download)
    db.commit()
    db.refresh(db_download)

def get_downloads(user_id: int, db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Download).filter(
        models.Download.user_id == user_id
        ).offset(skip).limit(limit).all()

def get_download(db: Session, model_id: int, user_id: int):
    return db.query(models.Download).filter(
        models.Download.model_id == model_id,
        models.Download.user_id == user_id
        ).first()
