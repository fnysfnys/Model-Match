import os
from typing import List
from fastapi import Depends, HTTPException, APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_current_user

from .. import crud, schemas

router = APIRouter(
    prefix="/api/feedback",
    tags=["feedback"]
)

@router.post("/{model_id}/submit-feedback",
response_model=schemas.feedback.Feedback
)
def submit_feedback(
    feedback: schemas.feedback.FeedbackBase,
    model_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """Takes in feedback for the given model and writes it to the database"""
    
    db_model = crud.models.get_model_by_id(db=db, id=model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")

    return crud.feedback.create_feedback(
        db=db,
        feedback=feedback,
        model_id=model_id,
        user_id=current_user.id
        )

@router.get("/{model_id}", response_model=List[schemas.feedback.Feedback])
def read_model_feedback(
    model_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """
    Returns all records of feedback for the corresponding model by its id.
    """

    db_model = crud.models.get_model_by_id(db=db, id=model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    feedback = crud.feedback.get_model_feedback(
        model_id=model_id,
        db=db,
        skip=skip,limit=limit
        )
    return feedback

@router.delete("/delete-feedback")
def delete_model(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.users.User = Depends(get_current_user)
    ):

    """
    Verifies the user requesting the delete is the one who submitted the
    feedback, if so, deletes the record of the feedback
    """

    db_feedback = crud.feedback.get_feedback_by_id(db, id=feedback_id)
    if db_feedback is None:
        raise HTTPException(status_code=404, detail="Feedback not found")
    if db_feedback.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Unauthorised")
    crud.feedback.delete_feedback(db=db, id=feedback_id)
    return {"ok": True}
