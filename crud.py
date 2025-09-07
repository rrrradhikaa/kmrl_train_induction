from sqlalchemy.orm import Session
from models import Train, Alert

def get_all_trains(db: Session):
    return db.query(Train).all()

def get_train_by_id(db: Session, train_id: int):
    return db.query(Train).filter(Train.id == train_id).first()

def get_all_alerts(db: Session):
    return db.query(Alert).all()
