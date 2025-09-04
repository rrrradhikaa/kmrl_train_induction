from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from kmrl_train_induction.api.deps import get_db
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api.schemas import (
    MileageBalancingOut, MileageBalancingCreate, MileageBalancingUpdate
)

router = APIRouter(prefix="/mileage-balancing", tags=["Mileage Balancing"])

@router.get("/", response_model=List[MileageBalancingOut])
def list_mileage(
    train_id: Optional[str] = None,
    coach_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(models.MileageBalancing)
    if train_id: q = q.filter(models.MileageBalancing.train_id == train_id)
    if coach_id: q = q.filter(models.MileageBalancing.coach_id == coach_id)
    return q.order_by(models.MileageBalancing.id.desc()).offset(offset).limit(limit).all()

@router.get("/{item_id}", response_model=MileageBalancingOut)
def get_mileage(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.MileageBalancing).get(item_id)
    if not obj: raise HTTPException(404, "MileageBalancing not found")
    return obj

@router.post("/", response_model=MileageBalancingOut, status_code=201)
def create_mileage(payload: MileageBalancingCreate, db: Session = Depends(get_db)):
    obj = models.MileageBalancing(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.patch("/{item_id}", response_model=MileageBalancingOut)
def update_mileage(item_id: int, payload: MileageBalancingUpdate, db: Session = Depends(get_db)):
    obj = db.query(models.MileageBalancing).get(item_id)
    if not obj: raise HTTPException(404, "MileageBalancing not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{item_id}", status_code=204)
def delete_mileage(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.MileageBalancing).get(item_id)
    if not obj: raise HTTPException(404, "MileageBalancing not found")
    db.delete(obj); db.commit()
    return None
