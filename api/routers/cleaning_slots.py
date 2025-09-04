from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from kmrl_train_induction.api.deps import get_db
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api.schemas import CleaningSlotOut, CleaningSlotCreate, CleaningSlotUpdate

router = APIRouter(prefix="/cleaning-slots", tags=["Cleaning Slots"])

@router.get("/", response_model=List[CleaningSlotOut])
def list_cleaning(
    train_id: Optional[str] = None,
    coach_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(models.CleaningSlot)
    if train_id: q = q.filter(models.CleaningSlot.train_id == train_id)
    if coach_id: q = q.filter(models.CleaningSlot.coach_id == coach_id)
    return q.order_by(models.CleaningSlot.id.desc()).offset(offset).limit(limit).all()

@router.get("/{item_id}", response_model=CleaningSlotOut)
def get_cleaning(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.CleaningSlot).get(item_id)
    if not obj: raise HTTPException(404, "CleaningSlot not found")
    return obj

@router.post("/", response_model=CleaningSlotOut, status_code=201)
def create_cleaning(payload: CleaningSlotCreate, db: Session = Depends(get_db)):
    obj = models.CleaningSlot(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.patch("/{item_id}", response_model=CleaningSlotOut)
def update_cleaning(item_id: int, payload: CleaningSlotUpdate, db: Session = Depends(get_db)):
    obj = db.query(models.CleaningSlot).get(item_id)
    if not obj: raise HTTPException(404, "CleaningSlot not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{item_id}", status_code=204)
def delete_cleaning(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.CleaningSlot).get(item_id)
    if not obj: raise HTTPException(404, "CleaningSlot not found")
    db.delete(obj); db.commit()
    return None
