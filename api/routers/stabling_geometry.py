from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api import schemas
from kmrl_train_induction.mock_api.database import get_db
from typing import List

router = APIRouter(
    prefix="/stabling_geometry",
    tags=["Stabling Geometry"]
)

@router.post("/", response_model=schemas.StablingGeometry)
def create_geometry(geo: schemas.StablingGeometryCreate, db: Session = Depends(get_db)):
    db_geo = models.StablingGeometry(**geo.dict())
    db.add(db_geo)
    db.commit()
    db.refresh(db_geo)
    return db_geo

@router.get("/", response_model=List[schemas.StablingGeometry])
def get_geometries(db: Session = Depends(get_db)):
    return db.query(models.StablingGeometry).all()

@router.get("/{id}", response_model=schemas.StablingGeometry)
def get_geometry(id: int, db: Session = Depends(get_db)):
    geo = db.query(models.StablingGeometry).filter(models.StablingGeometry.id == id).first()
    if not geo:
        raise HTTPException(status_code=404, detail="Geometry not found")
    return geo

@router.delete("/{id}")
def delete_geometry(id: int, db: Session = Depends(get_db)):
    geo = db.query(models.StablingGeometry).filter(models.StablingGeometry.id == id).first()
    if not geo:
        raise HTTPException(status_code=404, detail="Geometry not found")
    db.delete(geo)
    db.commit()
    return {"message": "Geometry deleted successfully"}
