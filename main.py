from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas

# Create tables in DB if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="KMRL Real-time API")


# --------------------
# DB session dependency
# --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------
# Root route
# --------------------
@app.get("/")
def root():
    return {"message": "KMRL Real-time API is running"}


# --------------------
# TRAINS CRUD
# --------------------
@app.get("/trains", response_model=list[schemas.TrainResponse])
def read_trains(db: Session = Depends(get_db)):
    return db.query(models.Train).all()


@app.get("/trains/{train_id}", response_model=schemas.TrainResponse)
def read_train(train_id: int, db: Session = Depends(get_db)):
    train = db.query(models.Train).filter(models.Train.id == train_id).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    return train


@app.post("/trains", response_model=schemas.TrainResponse)
def create_train(train: schemas.TrainCreate, db: Session = Depends(get_db)):
    db_train = models.Train(**train.dict())
    db.add(db_train)
    db.commit()
    db.refresh(db_train)
    return db_train


@app.put("/trains/{train_id}", response_model=schemas.TrainResponse)
def update_train(train_id: int, updated: schemas.TrainUpdate, db: Session = Depends(get_db)):
    train = db.query(models.Train).filter(models.Train.id == train_id).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(train, key, value)
    db.commit()
    db.refresh(train)
    return train


@app.delete("/trains/{train_id}")
def delete_train(train_id: int, db: Session = Depends(get_db)):
    train = db.query(models.Train).filter(models.Train.id == train_id).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train not found")
    db.delete(train)
    db.commit()
    return {"message": "Train deleted successfully"}


# --------------------
# ALERTS CRUD
# --------------------
@app.get("/alerts", response_model=list[schemas.AlertResponse])
def read_alerts(db: Session = Depends(get_db)):
    return db.query(models.Alert).all()


@app.get("/alerts/{alert_id}", response_model=schemas.AlertResponse)
def read_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@app.post("/alerts", response_model=schemas.AlertResponse)
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


@app.put("/alerts/{alert_id}", response_model=schemas.AlertResponse)
def update_alert(alert_id: int, updated: schemas.AlertUpdate, db: Session = Depends(get_db)):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(alert, key, value)
    db.commit()
    db.refresh(alert)
    return alert


@app.delete("/alerts/{alert_id}")
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(models.Alert).filter(models.Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(alert)
    db.commit()
    return {"message": "Alert deleted successfully"}





