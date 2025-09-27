from sqlalchemy.orm import Session
from models import JobCard
from schemas import JobCardCreate
from typing import List, Optional
from datetime import datetime

def read_job_card(db: Session, job_id: int) -> Optional[JobCard]:
    return db.query(JobCard).filter(JobCard.id == job_id).first()

def read_job_cards(db: Session, skip: int = 0, limit: int = 100) -> List[JobCard]:
    return db.query(JobCard).offset(skip).limit(limit).all()

def read_job_cards_by_train(db: Session, train_id: int) -> List[JobCard]:
    return db.query(JobCard).filter(JobCard.train_id == train_id).all()

def read_open_job_cards(db: Session, train_id: int = None) -> List[JobCard]:
    query = db.query(JobCard).filter(JobCard.status == "open")
    if train_id:
        query = query.filter(JobCard.train_id == train_id)
    return query.all()

def create_job_card(db: Session, job_card: JobCardCreate) -> JobCard:
    db_job_card = JobCard(
        train_id=job_card.train_id,
        work_order_id=job_card.work_order_id,
        status=job_card.status,
        description=job_card.description
    )
    db.add(db_job_card)
    db.commit()
    db.refresh(db_job_card)
    return db_job_card

def update_job_card(db: Session, job_id: int, job_data: dict) -> Optional[JobCard]:
    db_job_card = db.query(JobCard).filter(JobCard.id == job_id).first()
    if db_job_card:
        for key, value in job_data.items():
            if key == "status" and value == "closed":
                setattr(db_job_card, "closed_at", datetime.now())
            setattr(db_job_card, key, value)
        db.commit()
        db.refresh(db_job_card)
    return db_job_card

def delete_job_card(db: Session, job_id: int) -> bool:
    db_job_card = db.query(JobCard).filter(JobCard.id == job_id).first()
    if db_job_card:
        db.delete(db_job_card)
        db.commit()
        return True
    return False

def close_job_card(db: Session, job_id: int) -> Optional[JobCard]:
    return update_job_card(db, job_id, {"status": "closed"})

def check_open_job_cards(db: Session, train_id: int) -> bool:
    open_jobs = read_open_job_cards(db, train_id)
    return len(open_jobs) > 0