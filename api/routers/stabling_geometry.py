from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from kmrl_train_induction.mock_api import models
from kmrl_train_induction.api import schemas
from kmrl_train_induction.mock_api.database import get_db

router = APIRouter(
    prefix="/stabling_geometry",
    tags=["Stabling Geometry"]
)

# -----------------------------
# CREATE
# -----------------------------
@router.post("/", response_model=schemas.StablingGeometry)
def create_geometry(geo: schemas.StablingGeometryCreate, db: Session = Depends(get_db)):
    db_geo = models.StablingGeometry(**geo.dict())
    db.add(db_geo)
    db.commit()
    db.refresh(db_geo)
    return db_geo

# -----------------------------
# READ ALL
# -----------------------------
@router.get("/", response_model=List[schemas.StablingGeometry])
def get_geometries(db: Session = Depends(get_db)):
    return db.query(models.StablingGeometry).all()

# -----------------------------
# READ ONE
# -----------------------------
@router.get("/{id}", response_model=schemas.StablingGeometry)
def get_geometry(id: int, db: Session = Depends(get_db)):
    geo = db.query(models.StablingGeometry).filter(models.StablingGeometry.id == id).first()
    if not geo:
        raise HTTPException(status_code=404, detail="Geometry not found")
    return geo

# -----------------------------
# DELETE
# -----------------------------
@router.delete("/{id}")
def delete_geometry(id: int, db: Session = Depends(get_db)):
    geo = db.query(models.StablingGeometry).filter(models.StablingGeometry.id == id).first()
    if not geo:
        raise HTTPException(status_code=404, detail="Geometry not found")
    db.delete(geo)
    db.commit()
    return {"message": "Geometry deleted successfully"}

# -----------------------------
# PATCH (UPDATE)
# -----------------------------
@router.patch("/{id}", response_model=schemas.StablingGeometry)
def update_geometry(
    id: int,
    updates: schemas.StablingGeometryUpdate,
    db: Session = Depends(get_db)
):
    geo = db.query(models.StablingGeometry).filter(models.StablingGeometry.id == id).first()
    if not geo:
        raise HTTPException(status_code=404, detail="Geometry not found")

    # Only update fields provided in the PATCH payload
    update_data = updates.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(geo, key, value)

    db.commit()
    db.refresh(geo)
    return geo
