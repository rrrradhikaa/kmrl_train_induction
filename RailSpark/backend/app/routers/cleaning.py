from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from database import get_db
from schemas import CleaningSlotCreate, CleaningSlotResponse
import crud

router = APIRouter(prefix="/cleaning", tags=["cleaning slots"])

@router.post("/", response_model=CleaningSlotResponse, status_code=status.HTTP_201_CREATED)
def create_cleaning_slot(slot: CleaningSlotCreate, db: Session = Depends(get_db)):
    # Verify train exists
    db_train = crud.trains.read_train(db, train_id=slot.train_id)
    if not db_train:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Train not found"
        )
    
    # Check if bay is available
    existing_slots = crud.cleaning.check_bay_availability(db, bay_number=slot.bay_number, slot_time=slot.slot_time)
    if existing_slots:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bay is already occupied at this time"
        )
    
    return crud.cleaning.create_cleaning_slot(db=db, slot=slot)

@router.get("/", response_model=List[CleaningSlotResponse])
def read_cleaning_slots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    slots = crud.cleaning.read_cleaning_slots(db, skip=skip, limit=limit)
    return slots

@router.get("/train/{train_id}", response_model=List[CleaningSlotResponse])
def read_slots_by_train(train_id: int, db: Session = Depends(get_db)):
    slots = crud.cleaning.read_slots_by_train(db, train_id=train_id)
    return slots

@router.get("/date/{slot_date}", response_model=List[CleaningSlotResponse])
def read_slots_by_date(slot_date: date, db: Session = Depends(get_db)):
    slots = crud.cleaning.read_slots_by_date(db, slot_date=slot_date)
    return slots

@router.get("/availability")
def check_bay_availability(bay_number: int, slot_time: str, db: Session = Depends(get_db)):
    from datetime import datetime
    try:
        slot_datetime = datetime.fromisoformat(slot_time)
        existing_slots = crud.cleaning.check_bay_availability(db, bay_number=bay_number, slot_time=slot_datetime)
        return {
            "bay_number": bay_number,
            "slot_time": slot_time,
            "available": len(existing_slots) == 0,
            "message": "Bay is available" if len(existing_slots) == 0 else "Bay is occupied"
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid datetime format. Use ISO format: YYYY-MM-DDTHH:MM:SS"
        )

@router.get("/{slot_id}", response_model=CleaningSlotResponse)
def read_cleaning_slot(slot_id: int, db: Session = Depends(get_db)):
    db_slot = crud.cleaning.read_cleaning_slot(db, slot_id=slot_id)
    if db_slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cleaning slot not found"
        )
    return db_slot

@router.put("/{slot_id}", response_model=CleaningSlotResponse)
def update_cleaning_slot(slot_id: int, slot_data: CleaningSlotCreate, db: Session = Depends(get_db)):
    db_slot = crud.cleaning.read_cleaning_slot(db, slot_id=slot_id)
    if db_slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cleaning slot not found"
        )
    return crud.cleaning.update_cleaning_slot(db=db, slot_id=slot_id, slot_data=slot_data.dict())

@router.patch("/{slot_id}/complete", response_model=CleaningSlotResponse)
def complete_cleaning_slot(slot_id: int, db: Session = Depends(get_db)):
    db_slot = crud.cleaning.read_cleaning_slot(db, slot_id=slot_id)
    if db_slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cleaning slot not found"
        )
    return crud.cleaning.complete_cleaning_slot(db=db, slot_id=slot_id)

@router.delete("/{slot_id}")
def delete_cleaning_slot(slot_id: int, db: Session = Depends(get_db)):
    db_slot = crud.cleaning.read_cleaning_slot(db, slot_id=slot_id)
    if db_slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cleaning slot not found"
        )
    crud.cleaning.delete_cleaning_slot(db=db, slot_id=slot_id)
    return {"message": "Cleaning slot deleted successfully"}