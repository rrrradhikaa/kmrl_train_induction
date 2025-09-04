from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from kmrl_train_induction.api.deps import get_db
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api.schemas import (
    StablingGeometryOut, StablingGeometryCreate, StablingGeometryUpdate
)

router = APIRouter(prefix="/stabling-geometry", tags=["Stabling Geometry"])

@router.get("/", response_model=List[StablingGeometryOut])
def list_stabling(
    train_id: Optional[str] = None,
    coach_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(models.StablingGeometry)
    if train_id: q = q.filter(models.StablingGeometry.train_id == train_id)
    if coach_id: q = q.filter(models.StablingGeometry.coach_id == coach_id)
    return q.order_by(models.StablingGeometry.id.desc()).offset(offset).limit(limit).all()

@router.get("/{item_id}", response_model=StablingGeometryOut)
def get_stabling(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.StablingGeometry).get(item_id)
    if not obj: raise HTTPException(404, "StablingGeometry not found")
    return obj

@router.post("/", response_model=StablingGeometryOut, status_code=201)
def create_stabling(payload: StablingGeometryCreate, db: Session = Depends(get_db)):
    obj = models.StablingGeometry(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.patch("/{item_id}", response_model=StablingGeometryOut)
def update_stabling(item_id: int, payload: StablingGeometryUpdate, db: Session = Depends(get_db)):
    obj = db.query(models.StablingGeometry).get(item_id)
    if not obj: raise HTTPException(404, "StablingGeometry not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit(); db.refresh(obj)
    return obj

@router.delete("/{item_id}", status_code=204)
def delete_stabling(item_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.StablingGeometry).get(item_id)
    if not obj: raise HTTPException(404, "StablingGeometry not found")
    db.delete(obj); db.commit()
    return None
