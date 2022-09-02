from sqlalchemy.orm import Session

from .. import models, schemas

def create_feedback(
    db: Session,
    feedback: schemas.feedback.FeedbackCreate,
    model_id: int,
    user_id: int
    ):
    db_feedback = models.Feedback(
        **feedback.dict(),
        model_id=model_id,
        user_id=user_id
        )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_model_feedback(
    model_id: int,
    db: Session,
    skip: int = 0,
    limit: int = 100
    ):
    return db.query(models.Feedback).filter(
        models.Feedback.model_id == model_id
        ).offset(skip).limit(limit).all()

def get_feedback_by_id(db: Session, id: int):
    return db.query(models.Feedback).filter(models.Feedback.id == id).first()

def delete_feedback(db: Session, id: int):
    db.query(models.Feedback).filter(models.Feedback.id == id).delete()
    db.commit()
