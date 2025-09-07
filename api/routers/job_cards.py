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
        # return the full SQLAlchemy error so we can debug
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
