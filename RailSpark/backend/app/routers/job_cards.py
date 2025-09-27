from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import JobCardCreate, JobCardResponse
import crud

router = APIRouter(prefix="/job-cards", tags=["job cards"])

@router.post("/", response_model=JobCardResponse, status_code=status.HTTP_201_CREATED)
def create_job_card(job_card: JobCardCreate, db: Session = Depends(get_db)):
    # Verify train exists
    db_train = crud.trains.read_train(db, train_id=job_card.train_id)
    if not db_train:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Train not found"
        )
    return crud.job_cards.create_job_card(db=db, job_card=job_card)

@router.get("/", response_model=List[JobCardResponse])
def read_job_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    job_cards = crud.job_cards.read_job_cards(db, skip=skip, limit=limit)
    return job_cards

@router.get("/train/{train_id}", response_model=List[JobCardResponse])
def read_job_cards_by_train(train_id: int, db: Session = Depends(get_db)):
    job_cards = crud.job_cards.read_job_cards_by_train(db, train_id=train_id)
    return job_cards

@router.get("/open", response_model=List[JobCardResponse])
def read_open_job_cards(train_id: int = None, db: Session = Depends(get_db)):
    job_cards = crud.job_cards.read_open_job_cards(db, train_id=train_id)
    return job_cards

@router.get("/{job_id}", response_model=JobCardResponse)
def read_job_card(job_id: int, db: Session = Depends(get_db)):
    db_job_card = crud.job_cards.read_job_card(db, job_id=job_id)
    if db_job_card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job card not found"
        )
    return db_job_card

@router.put("/{job_id}", response_model=JobCardResponse)
def update_job_card(job_id: int, job_data: JobCardCreate, db: Session = Depends(get_db)):
    db_job_card = crud.job_cards.read_job_card(db, job_id=job_id)
    if db_job_card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job card not found"
        )
    return crud.job_cards.update_job_card(db=db, job_id=job_id, job_data=job_data.dict())

@router.patch("/{job_id}/close", response_model=JobCardResponse)
def close_job_card(job_id: int, db: Session = Depends(get_db)):
    db_job_card = crud.job_cards.read_job_card(db, job_id=job_id)
    if db_job_card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job card not found"
        )
    return crud.job_cards.close_job_card(db=db, job_id=job_id)

@router.delete("/{job_id}")
def delete_job_card(job_id: int, db: Session = Depends(get_db)):
    db_job_card = crud.job_cards.read_job_card(db, job_id=job_id)
    if db_job_card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job card not found"
        )
    crud.job_cards.delete_job_card(db=db, job_id=job_id)
    return {"message": "Job card deleted successfully"}

@router.get("/train/{train_id}/has-open-jobs")
def check_open_job_cards(train_id: int, db: Session = Depends(get_db)):
    has_open_jobs = crud.job_cards.check_open_job_cards(db, train_id=train_id)
    return {
        "train_id": train_id,
        "has_open_job_cards": has_open_jobs,
        "message": "Train has open job cards" if has_open_jobs else "No open job cards"
    }