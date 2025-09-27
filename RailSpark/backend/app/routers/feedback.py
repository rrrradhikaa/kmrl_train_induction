from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import UserFeedbackCreate, UserFeedbackResponse
import crud

router = APIRouter(prefix="/feedback", tags=["user feedback"])

@router.post("/", response_model=UserFeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_feedback(feedback: UserFeedbackCreate, db: Session = Depends(get_db)):
    return crud.feedback.create_feedback(db=db, feedback=feedback)

@router.get("/", response_model=List[UserFeedbackResponse])
def read_all_feedback(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feedback_list = crud.feedback.read_all_feedback(db, skip=skip, limit=limit)
    return feedback_list

@router.get("/user/{user_id}", response_model=List[UserFeedbackResponse])
def read_feedback_by_user(user_id: int, db: Session = Depends(get_db)):
    feedback_list = crud.feedback.read_feedback_by_user(db, user_id=user_id)
    return feedback_list

@router.get("/recent", response_model=List[UserFeedbackResponse])
def read_recent_feedback(days: int = 7, db: Session = Depends(get_db)):
    feedback_list = crud.feedback.read_recent_feedback(db, days=days)
    return feedback_list

@router.get("/{feedback_id}", response_model=UserFeedbackResponse)
def read_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = crud.feedback.read_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    return db_feedback

@router.put("/{feedback_id}", response_model=UserFeedbackResponse)
def update_feedback(feedback_id: int, feedback_data: UserFeedbackCreate, db: Session = Depends(get_db)):
    db_feedback = crud.feedback.read_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    return crud.feedback.update_feedback(db=db, feedback_id=feedback_id, feedback_data=feedback_data.dict())

@router.delete("/{feedback_id}")
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    db_feedback = crud.feedback.read_feedback(db, feedback_id=feedback_id)
    if db_feedback is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    crud.feedback.delete_feedback(db=db, feedback_id=feedback_id)
    return {"message": "Feedback deleted successfully"}