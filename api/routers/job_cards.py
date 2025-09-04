from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api import schemas
from kmrl_train_induction.mock_api.database import get_db
from typing import List

router = APIRouter(
    prefix="/job_cards",
    tags=["Job Cards"]
)

@router.post("/", response_model=schemas.JobCard)
def create_job(job: schemas.JobCardCreate, db: Session = Depends(get_db)):
    db_job = models.JobCard(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=List[schemas.JobCard])
def get_jobs(db: Session = Depends(get_db)):
    return db.query(models.JobCard).all()

@router.get("/{job_id}", response_model=schemas.JobCard)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(models.JobCard).filter(models.JobCard.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.delete("/{job_id}")
def delete_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(models.JobCard).filter(models.JobCard.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"message": "Job deleted successfully"}
