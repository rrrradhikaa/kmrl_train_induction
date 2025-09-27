from sqlalchemy.orm import Session
from models import Train
from schemas import TrainCreate
from typing import List, Optional

def read_train(db: Session, train_id: int) -> Optional[Train]:
    return db.query(Train).filter(Train.id == train_id).first()

def read_train_by_number(db: Session, train_number: str) -> Optional[Train]:
    return db.query(Train).filter(Train.train_number == train_number).first()

def read_trains(db: Session, skip: int = 0, limit: int = 100) -> List[Train]:
    return db.query(Train).offset(skip).limit(limit).all()

def read_active_trains(db: Session) -> List[Train]:
    return db.query(Train).filter(Train.status == "active").all()

def create_train(db: Session, train: TrainCreate) -> Train:
    db_train = Train(
        train_number=train.train_number,
        current_mileage=train.current_mileage,
        last_maintenance_date=train.last_maintenance_date,
        status=train.status
    )
    db.add(db_train)
    db.commit()
    db.refresh(db_train)
    return db_train

def update_train(db: Session, train_id: int, train_data: dict) -> Optional[Train]:
    db_train = db.query(Train).filter(Train.id == train_id).first()
    if db_train:
        for key, value in train_data.items():
            setattr(db_train, key, value)
        db.commit()
        db.refresh(db_train)
    return db_train

def delete_train(db: Session, train_id: int) -> bool:
    db_train = db.query(Train).filter(Train.id == train_id).first()
    if db_train:
        db.delete(db_train)
        db.commit()
        return True
    return False

def update_train_mileage(db: Session, train_id: int, additional_mileage: int) -> Optional[Train]:
    db_train = db.query(Train).filter(Train.id == train_id).first()
    if db_train:
        db_train.current_mileage += additional_mileage
        db.commit()
        db.refresh(db_train)
    return db_train