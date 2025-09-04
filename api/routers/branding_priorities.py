from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api import schemas
from kmrl_train_induction.mock_api.database import get_db
from typing import List

router = APIRouter(
    prefix="/branding_priorities",
    tags=["Branding Priorities"]
)

@router.post("/", response_model=schemas.BrandingPriority)
def create_priority(priority: schemas.BrandingPriorityCreate, db: Session = Depends(get_db)):
    db_priority = models.BrandingPriority(**priority.dict())
    db.add(db_priority)
    db.commit()
    db.refresh(db_priority)
    return db_priority

@router.get("/", response_model=List[schemas.BrandingPriority])
def get_priorities(db: Session = Depends(get_db)):
    return db.query(models.BrandingPriority).all()

@router.get("/{id}", response_model=schemas.BrandingPriority)
def get_priority(id: int, db: Session = Depends(get_db)):
    priority = db.query(models.BrandingPriority).filter(models.BrandingPriority.id == id).first()
    if not priority:
        raise HTTPException(status_code=404, detail="Priority not found")
    return priority

@router.delete("/{id}")
def delete_priority(id: int, db: Session = Depends(get_db)):
    priority = db.query(models.BrandingPriority).filter(models.BrandingPriority.id == id).first()
    if not priority:
        raise HTTPException(status_code=404, detail="Priority not found")
    db.delete(priority)
    db.commit()
    return {"message": "Priority deleted successfully"}
