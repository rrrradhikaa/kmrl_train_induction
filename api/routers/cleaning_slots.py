from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api import schemas
from kmrl_train_induction.mock_api.database import get_db

router = APIRouter(
    prefix="/cleaning_slots",
    tags=["Cleaning Slots"]
)

# -----------------------------
# CREATE
# -----------------------------
@router.post("/", response_model=schemas.CleaningSlot)
def create_slot(slot: schemas.CleaningSlotCreate, db: Session = Depends(get_db)):
    db_slot = models.CleaningSlot(**slot.dict())
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

# -----------------------------
# READ ALL
# -----------------------------
@router.get("/", response_model=List[schemas.CleaningSlot])
def get_slots(db: Session = Depends(get_db)):
    return db.query(models.CleaningSlot).all()

# -----------------------------
# READ ONE
# -----------------------------
@router.get("/{id}", response_model=schemas.CleaningSlot)
def get_slot(id: int, db: Session = Depends(get_db)):
    slot = db.query(models.CleaningSlot).filter(models.CleaningSlot.id == id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    return slot

# -----------------------------
# DELETE
# -----------------------------
@router.delete("/{id}")
def delete_slot(id: int, db: Session = Depends(get_db)):
    slot = db.query(models.CleaningSlot).filter(models.CleaningSlot.id == id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    db.delete(slot)
    db.commit()
    return {"message": "Slot deleted successfully"}

# -----------------------------
# PATCH (UPDATE)
# -----------------------------
@router.patch("/{id}", response_model=schemas.CleaningSlot)
def update_slot(
    id: int,
    updates: schemas.CleaningSlotUpdate,
    db: Session = Depends(get_db)
):
    slot = db.query(models.CleaningSlot).filter(models.CleaningSlot.id == id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    # Only update fields provided in the PATCH payload
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(slot, key, value)

    db.commit()
    db.refresh(slot)
    return slot
