from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from kmrl_train_induction.api.deps import get_db
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api.schemas import JobCardOut, JobCardCreate, JobCardUpdate

router = APIRouter(prefix="/job-cards", tags=["Job Cards"])

@router.get("/", response_model=List[JobCardOut])
def list_jobs(
    train_id: Optional[str] = None,
    coach_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(models.JobCard)
    if train_id: q = q.filter(models.JobCard.train_id == train_id)
    if coach_id: q = q.filter(models.JobCard.coach_id == coach_id)
    if status: q = q.filter(models.JobCard.status == status)
    return q.order_by(models.JobCard.id.desc()).offset(offset).limit(limit).all()

@router.get("/{item_id}", response_model=JobCardOut)
def get_job(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.JobCard).get(item_id)
    if not obj: raise HTTPException(404, "JobCard not found")
    return obj

@router.post("/", response_model=JobCardOut, status_code=201)
def create_job(payload: JobCardCreate, db: Session = Depends(get_db)):
    obj = models.JobCard(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.patch("/{item_id}", response_model=JobCardOut)
def update_job(item_id: int, payload: JobCardUpdate, db: Session = Depends(get_db)):
    obj = db.query(models.JobCard).get(item_id)
    if not obj: raise HTTPException(404, "JobCard not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{item_id}", status_code=204)
def delete_job(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.JobCard).get(item_id)
    if not obj: raise HTTPException(404, "JobCard not found")
    db.delete(obj); db.commit()
    return None
