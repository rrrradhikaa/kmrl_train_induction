from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api import schemas
from kmrl_train_induction.mock_api.database import get_db
from typing import List

router = APIRouter(
    prefix="/cleaning_slots",
    tags=["Cleaning Slots"]
)

@router.post("/", response_model=schemas.CleaningSlot)
def create_slot(slot: schemas.CleaningSlotCreate, db: Session = Depends(get_db)):
    db_slot = models.CleaningSlot(**slot.dict())
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

@router.get("/", response_model=List[schemas.CleaningSlot])
def get_slots(db: Session = Depends(get_db)):
    return db.query(models.CleaningSlot).all()

@router.get("/{id}", response_model=schemas.CleaningSlot)
def get_slot(id: int, db: Session = Depends(get_db)):
    slot = db.query(models.CleaningSlot).filter(models.CleaningSlot.id == id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    return slot

@router.delete("/{id}")
def delete_slot(id: int, db: Session = Depends(get_db)):
    slot = db.query(models.CleaningSlot).filter(models.CleaningSlot.id == id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    db.delete(slot)
    db.commit()
    return {"message": "Slot deleted successfully"}
