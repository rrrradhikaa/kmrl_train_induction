from sqlalchemy.orm import Session
from models import CleaningSlot
from schemas import CleaningSlotCreate
from typing import List, Optional
from datetime import datetime, date

def read_cleaning_slot(db: Session, slot_id: int) -> Optional[CleaningSlot]:
    return db.query(CleaningSlot).filter(CleaningSlot.id == slot_id).first()

def read_cleaning_slots(db: Session, skip: int = 0, limit: int = 100) -> List[CleaningSlot]:
    return db.query(CleaningSlot).offset(skip).limit(limit).all()

def read_slots_by_train(db: Session, train_id: int) -> List[CleaningSlot]:
    return db.query(CleaningSlot).filter(CleaningSlot.train_id == train_id).all()

def read_slots_by_date(db: Session, slot_date: date) -> List[CleaningSlot]:
    start_datetime = datetime.combine(slot_date, datetime.min.time())
    end_datetime = datetime.combine(slot_date, datetime.max.time())
    return db.query(CleaningSlot).filter(
        CleaningSlot.slot_time >= start_datetime,
        CleaningSlot.slot_time <= end_datetime
    ).all()

def check_bay_availability(db: Session, bay_number: int, slot_time: datetime) -> List[CleaningSlot]:
    """Check if a bay is available at a given time"""
    return db.query(CleaningSlot).filter(
        CleaningSlot.bay_number == bay_number,
        CleaningSlot.slot_time == slot_time,
        CleaningSlot.status == "scheduled"
    ).all()

def create_cleaning_slot(db: Session, slot: CleaningSlotCreate) -> CleaningSlot:
    db_slot = CleaningSlot(
        train_id=slot.train_id,
        slot_time=slot.slot_time,
        bay_number=slot.bay_number,
        manpower_required=slot.manpower_required,
        status=slot.status
    )
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

def update_cleaning_slot(db: Session, slot_id: int, slot_data: dict) -> Optional[CleaningSlot]:
    db_slot = db.query(CleaningSlot).filter(CleaningSlot.id == slot_id).first()
    if db_slot:
        for key, value in slot_data.items():
            setattr(db_slot, key, value)
        db.commit()
        db.refresh(db_slot)
    return db_slot

def delete_cleaning_slot(db: Session, slot_id: int) -> bool:
    db_slot = db.query(CleaningSlot).filter(CleaningSlot.id == slot_id).first()
    if db_slot:
        db.delete(db_slot)
        db.commit()
        return True
    return False

def complete_cleaning_slot(db: Session, slot_id: int) -> Optional[CleaningSlot]:
    return update_cleaning_slot(db, slot_id, {"status": "completed"})