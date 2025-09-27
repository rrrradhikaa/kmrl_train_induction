from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import TrainCreate, TrainResponse
import crud

router = APIRouter(prefix="/trains", tags=["trains"])

@router.post("/", response_model=TrainResponse, status_code=status.HTTP_201_CREATED)
def create_train(train: TrainCreate, db: Session = Depends(get_db)):
    # Check if train number already exists
    db_train = crud.trains.read_train_by_number(db, train_number=train.train_number)
    if db_train:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Train number already registered"
        )
    return crud.trains.create_train(db=db, train=train)

@router.get("/", response_model=List[TrainResponse])
def read_trains(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    trains = crud.trains.read_trains(db, skip=skip, limit=limit)
    return trains

@router.get("/active", response_model=List[TrainResponse])
def read_active_trains(db: Session = Depends(get_db)):
    trains = crud.trains.read_active_trains(db)
    return trains

@router.get("/{train_id}", response_model=TrainResponse)
def read_train(train_id: int, db: Session = Depends(get_db)):
    db_train = crud.trains.read_train(db, train_id=train_id)
    if db_train is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Train not found"
        )
    return db_train

@router.put("/{train_id}", response_model=TrainResponse)
def update_train(train_id: int, train_data: TrainCreate, db: Session = Depends(get_db)):
    db_train = crud.trains.read_train(db, train_id=train_id)
    if db_train is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Train not found"
        )
    return crud.trains.update_train(db=db, train_id=train_id, train_data=train_data.dict())

@router.delete("/{train_id}")
def delete_train(train_id: int, db: Session = Depends(get_db)):
    db_train = crud.trains.read_train(db, train_id=train_id)
    if db_train is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Train not found"
        )
    crud.trains.delete_train(db=db, train_id=train_id)
    return {"message": "Train deleted successfully"}

@router.patch("/{train_id}/mileage")
def update_train_mileage(train_id: int, additional_mileage: int, db: Session = Depends(get_db)):
    db_train = crud.trains.read_train(db, train_id=train_id)
    if db_train is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Train not found"
        )
    updated_train = crud.trains.update_train_mileage(db=db, train_id=train_id, additional_mileage=additional_mileage)
    return {"message": f"Mileage updated successfully. New mileage: {updated_train.current_mileage}"}