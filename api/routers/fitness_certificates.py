from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api import schemas
from kmrl_train_induction.mock_api.database import get_db

router = APIRouter(
    prefix="/fitness_certificates",
    tags=["Fitness Certificates"]
)

# -----------------------------
# CREATE
# -----------------------------
@router.post("/", response_model=schemas.FitnessCertificate)
def create_certificate(
    cert: schemas.FitnessCertificateCreate, 
    db: Session = Depends(get_db)
):
    db_cert = models.FitnessCertificate(**cert.dict())
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert

# -----------------------------
# READ ALL
# -----------------------------
@router.get("/", response_model=List[schemas.FitnessCertificate])
def get_certificates(db: Session = Depends(get_db)):
    return db.query(models.FitnessCertificate).all()

# -----------------------------
# READ ONE
# -----------------------------
@router.get("/{certificate_id}", response_model=schemas.FitnessCertificate)
def get_certificate(certificate_id: str, db: Session = Depends(get_db)):
    cert = db.query(models.FitnessCertificate).filter(
        models.FitnessCertificate.certificate_id == certificate_id
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return cert

# -----------------------------
# DELETE
# -----------------------------
@router.delete("/{certificate_id}")
def delete_certificate(certificate_id: str, db: Session = Depends(get_db)):
    cert = db.query(models.FitnessCertificate).filter(
        models.FitnessCertificate.certificate_id == certificate_id
    ).first()
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    db.delete(cert)
    db.commit()
    return {"message": "Certificate deleted successfully"}

# -----------------------------
# PATCH (UPDATE)
# -----------------------------
@router.patch("/{certificate_id}", response_model=schemas.FitnessCertificate)
def update_certificate(
    certificate_id: str,
    updates: schemas.FitnessCertificateUpdate,
    db: Session = Depends(get_db)
):
    cert = db.query(models.FitnessCertificate).filter(
        models.FitnessCertificate.certificate_id == certificate_id
    ).first()

    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    # Only update fields provided in the PATCH payload
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cert, key, value)

    db.commit()
    db.refresh(cert)
    return cert
