from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api import schemas
from kmrl_train_induction.mock_api.database import get_db
from typing import List

router = APIRouter(
    prefix="/mileage_balancing",
    tags=["Mileage Balancing"]
)

@router.post("/", response_model=schemas.MileageBalancing)
def create_mileage(data: schemas.MileageBalancingCreate, db: Session = Depends(get_db)):
    db_data = models.MileageBalancing(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

@router.get("/", response_model=List[schemas.MileageBalancing])
def get_all_mileage(db: Session = Depends(get_db)):
    return db.query(models.MileageBalancing).all()

@router.get("/{id}", response_model=schemas.MileageBalancing)
def get_mileage(id: int, db: Session = Depends(get_db)):
    row = db.query(models.MileageBalancing).filter(models.MileageBalancing.id == id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Mileage record not found")
    return row

@router.delete("/{id}")
def delete_mileage(id: int, db: Session = Depends(get_db)):
    row = db.query(models.MileageBalancing).filter(models.MileageBalancing.id == id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Mileage record not found")
    db.delete(row)
    db.commit()
    return {"message": "Mileage record deleted successfully"}
