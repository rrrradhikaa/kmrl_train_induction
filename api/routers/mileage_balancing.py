from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api import schemas
from kmrl_train_induction.mock_api.database import get_db

router = APIRouter(
    prefix="/mileage_balancing",
    tags=["Mileage Balancing"]
)

# -----------------------------
# CREATE
# -----------------------------
@router.post("/", response_model=schemas.MileageBalancing)
def create_mileage(data: schemas.MileageBalancingCreate, db: Session = Depends(get_db)):
    db_data = models.MileageBalancing(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# -----------------------------
# READ ALL
# -----------------------------
@router.get("/", response_model=List[schemas.MileageBalancing])
def get_all_mileage(db: Session = Depends(get_db)):
    return db.query(models.MileageBalancing).all()

# -----------------------------
# READ ONE
# -----------------------------
@router.get("/{id}", response_model=schemas.MileageBalancing)
def get_mileage(id: int, db: Session = Depends(get_db)):
    row = db.query(models.MileageBalancing).filter(models.MileageBalancing.id == id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Mileage record not found")
    return row

# -----------------------------
# DELETE
# -----------------------------
@router.delete("/{id}")
def delete_mileage(id: int, db: Session = Depends(get_db)):
    row = db.query(models.MileageBalancing).filter(models.MileageBalancing.id == id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Mileage record not found")
    db.delete(row)
    db.commit()
    return {"message": "Mileage record deleted successfully"}

# -----------------------------
# PATCH (UPDATE)
# -----------------------------
@router.patch("/{id}", response_model=schemas.MileageBalancing)
def update_mileage(
    id: int,
    updates: schemas.MileageBalancingUpdate,
    db: Session = Depends(get_db)
):
    row = db.query(models.MileageBalancing).filter(models.MileageBalancing.id == id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Mileage record not found")

    # Only update fields provided in the PATCH payload
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(row, key, value)

    db.commit()
    db.refresh(row)
    return row
