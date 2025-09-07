from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api import schemas
from kmrl_train_induction.mock_api.database import get_db

router = APIRouter(
    prefix="/branding_priorities",
    tags=["Branding Priorities"]
)

# -----------------------------
# CREATE
# -----------------------------
@router.post("/", response_model=schemas.BrandingPriority)
def create_priority(priority: schemas.BrandingPriorityCreate, db: Session = Depends(get_db)):
    db_priority = models.BrandingPriority(**priority.dict())
    db.add(db_priority)
    db.commit()
    db.refresh(db_priority)
    return db_priority

# -----------------------------
# READ ALL
# -----------------------------
@router.get("/", response_model=List[schemas.BrandingPriority])
def get_priorities(db: Session = Depends(get_db)):
    return db.query(models.BrandingPriority).all()

# -----------------------------
# READ ONE
# -----------------------------
@router.get("/{id}", response_model=schemas.BrandingPriority)
def get_priority(id: int, db: Session = Depends(get_db)):
    priority = db.query(models.BrandingPriority).filter(models.BrandingPriority.id == id).first()
    if not priority:
        raise HTTPException(status_code=404, detail="Priority not found")
    return priority

# -----------------------------
# DELETE
# -----------------------------
@router.delete("/{id}")
def delete_priority(id: int, db: Session = Depends(get_db)):
    priority = db.query(models.BrandingPriority).filter(models.BrandingPriority.id == id).first()
    if not priority:
        raise HTTPException(status_code=404, detail="Priority not found")
    db.delete(priority)
    db.commit()
    return {"message": "Priority deleted successfully"}

# -----------------------------
# PATCH (UPDATE)
# -----------------------------
@router.patch("/{id}", response_model=schemas.BrandingPriority)
def update_priority(
    id: int,
    updates: schemas.BrandingPriorityUpdate,
    db: Session = Depends(get_db)
):
    priority = db.query(models.BrandingPriority).filter(models.BrandingPriority.id == id).first()
    if not priority:
        raise HTTPException(status_code=404, detail="Priority not found")

    # Only update fields provided in the PATCH payload
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(priority, key, value)

    db.commit()
    db.refresh(priority)
    return priority
