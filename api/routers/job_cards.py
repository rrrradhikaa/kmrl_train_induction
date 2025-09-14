# kmrl_train_induction/api/routers/job_cards.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api import schemas
from kmrl_train_induction.mock_api.database import get_db
from typing import List

router = APIRouter(
    prefix="/job_cards",
    tags=["Job Cards"]
)


# CREATE a new job card
@router.post("/", response_model=schemas.JobCard)
def create_job(job: schemas.JobCardCreate, db: Session = Depends(get_db)):
    try:
        db_job = models.JobCard(**job.dict())
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# GET all job cards
@router.get("/", response_model=List[schemas.JobCard])
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.JobCard).all()
    return jobs


# GET a single job card by ID
@router.get("/{job_id}", response_model=schemas.JobCard)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(models.JobCard).filter(models.JobCard.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job card not found")
    return job


# UPDATE a job card (partial update)
@router.patch("/{job_id}", response_model=schemas.JobCard)
def update_job(job_id: str, job_data: schemas.JobCardUpdate, db: Session = Depends(get_db)):
    job = db.query(models.JobCard).filter(models.JobCard.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job card not found")
    
    for key, value in job_data.dict(exclude_unset=True).items():
        setattr(job, key, value)
    
    try:
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# DELETE a job card
@router.delete("/{job_id}")
def delete_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(models.JobCard).filter(models.JobCard.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job card not found")
    try:
        db.delete(job)
        db.commit()
        return {"message": "Job card deleted successfully"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
