from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from kmrl_train_induction.api.deps import get_db
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api.schemas import (
    FitnessCertificateOut, FitnessCertificateCreate, FitnessCertificateUpdate
)

router = APIRouter(prefix="/fitness-certificates", tags=["Fitness Certificates"])

@router.get("/", response_model=List[FitnessCertificateOut])
def list_fc(
    train_id: Optional[str] = None,
    coach_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(models.FitnessCertificate)
    if train_id:
        q = q.filter(models.FitnessCertificate.train_id == train_id)
    if coach_id:
        q = q.filter(models.FitnessCertificate.coach_id == coach_id)
    return q.order_by(models.FitnessCertificate.certificate_id.desc()).offset(offset).limit(limit).all()

@router.get("/{certificate_id}", response_model=FitnessCertificateOut)
def get_fc(certificate_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.FitnessCertificate).get(certificate_id)
    if not obj:
        raise HTTPException(404, "FitnessCertificate not found")
    return obj

@router.post("/", response_model=FitnessCertificateOut, status_code=201)
def create_fc(payload: FitnessCertificateCreate, db: Session = Depends(get_db)):
    obj = models.FitnessCertificate(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.patch("/{certificate_id}", response_model=FitnessCertificateOut)
def update_fc(certificate_id: int, payload: FitnessCertificateUpdate, db: Session = Depends(get_db)):
    obj = db.query(models.FitnessCertificate).get(certificate_id)
    if not obj:
        raise HTTPException(404, "FitnessCertificate not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{certificate_id}", status_code=204)
def delete_fc(certificate_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.FitnessCertificate).get(certificate_id)
    if not obj:
        raise HTTPException(404, "FitnessCertificate not found")
    db.delete(obj)
    db.commit()
    return None
