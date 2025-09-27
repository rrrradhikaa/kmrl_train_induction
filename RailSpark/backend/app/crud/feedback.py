from sqlalchemy.orm import Session
from models import UserFeedback
from schemas import UserFeedbackCreate
from typing import List, Optional

def read_feedback(db: Session, feedback_id: int) -> Optional[UserFeedback]:
    return db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()

def read_all_feedback(db: Session, skip: int = 0, limit: int = 100) -> List[UserFeedback]:
    return db.query(UserFeedback).offset(skip).limit(limit).order_by(UserFeedback.created_at.desc()).all()

def read_feedback_by_user(db: Session, user_id: int) -> List[UserFeedback]:
    return db.query(UserFeedback).filter(UserFeedback.user_id == user_id).order_by(UserFeedback.created_at.desc()).all()

def create_feedback(db: Session, feedback: UserFeedbackCreate) -> UserFeedback:
    db_feedback = UserFeedback(
        user_id=feedback.user_id,
        feedback_text=feedback.feedback_text
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def update_feedback(db: Session, feedback_id: int, feedback_data: dict) -> Optional[UserFeedback]:
    db_feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if db_feedback:
        for key, value in feedback_data.items():
            setattr(db_feedback, key, value)
        db.commit()
        db.refresh(db_feedback)
    return db_feedback

def delete_feedback(db: Session, feedback_id: int) -> bool:
    db_feedback = db.query(UserFeedback).filter(UserFeedback.id == feedback_id).first()
    if db_feedback:
        db.delete(db_feedback)
        db.commit()
        return True
    return False

def read_recent_feedback(db: Session, days: int = 7) -> List[UserFeedback]:
    from datetime import datetime, timedelta
    since_date = datetime.now() - timedelta(days=days)
    return db.query(UserFeedback).filter(UserFeedback.created_at >= since_date).order_by(UserFeedback.created_at.desc()).all()