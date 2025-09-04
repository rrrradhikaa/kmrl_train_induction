from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from kmrl_train_induction.api.deps import get_db
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api.schemas import (
    BrandingPriorityOut, BrandingPriorityCreate, BrandingPriorityUpdate
)

router = APIRouter(prefix="/branding-priorities", tags=["Branding Priorities"])

@router.get("/", response_model=List[BrandingPriorityOut])
def list_branding(
    train_id: Optional[str] = None,
    coach_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(models.BrandingPriority)
    if train_id: q = q.filter(models.BrandingPriority.train_id == train_id)
    if coach_id: q = q.filter(models.BrandingPriority.coach_id == coach_id)
    return q.order_by(models.BrandingPriority.priority.asc().nulls_last()).offset(offset).limit(limit).all()

@router.get("/{item_id}", response_model=BrandingPriorityOut)
def get_branding(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.BrandingPriority).get(item_id)
    if not obj: raise HTTPException(404, "BrandingPriority not found")
    return obj

@router.post("/", response_model=BrandingPriorityOut, status_code=201)
def create_branding(payload: BrandingPriorityCreate, db: Session = Depends(get_db)):
    obj = models.BrandingPriority(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.patch("/{item_id}", response_model=BrandingPriorityOut)
def update_branding(item_id: int, payload: BrandingPriorityUpdate, db: Session = Depends(get_db)):
    obj = db.query(models.BrandingPriority).get(item_id)
    if not obj: raise HTTPException(404, "BrandingPriority not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{item_id}", status_code=204)
def delete_branding(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.BrandingPriority).get(item_id)
    if not obj: raise HTTPException(404, "BrandingPriority not found")
    db.delete(obj); db.commit()
    return None
