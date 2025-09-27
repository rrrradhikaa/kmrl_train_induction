from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import StablingGeometryCreate, StablingGeometryResponse
import crud

router = APIRouter(prefix="/stabling", tags=["stabling geometry"])

@router.post("/", response_model=StablingGeometryResponse, status_code=status.HTTP_201_CREATED)
def create_stabling_geometry(geometry: StablingGeometryCreate, db: Session = Depends(get_db)):
    # Verify train exists
    db_train = crud.trains.read_train(db, train_id=geometry.train_id)
    if not db_train:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Train not found"
        )
    return crud.stabling.create_stabling_geometry(db=db, geometry=geometry)

@router.get("/", response_model=List[StablingGeometryResponse])
def read_stabling_geometries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    geometries = crud.stabling.read_stabling_geometries(db, skip=skip, limit=limit)
    return geometries

@router.get("/train/{train_id}", response_model=StablingGeometryResponse)
def read_geometry_by_train(train_id: int, db: Session = Depends(get_db)):
    geometry = crud.stabling.read_geometry_by_train(db, train_id=train_id)
    if geometry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No stabling geometry found for this train"
        )
    return geometry

@router.get("/bay/{bay_position}", response_model=List[StablingGeometryResponse])
def read_trains_in_bay(bay_position: str, db: Session = Depends(get_db)):
    geometries = crud.stabling.read_trains_in_bay(db, bay_position=bay_position)
    return geometries

@router.get("/shunting-required", response_model=List[StablingGeometryResponse])
def read_bays_requiring_shunting(db: Session = Depends(get_db)):
    geometries = crud.stabling.read_bays_requiring_shunting(db)
    return geometries

@router.post("/optimize", response_model=List[StablingGeometryResponse])
def optimize_stabling_arrangement(db: Session = Depends(get_db)):
    optimized_geometries = crud.stabling.optimize_stabling_arrangement(db)
    return optimized_geometries

@router.get("/{geometry_id}", response_model=StablingGeometryResponse)
def read_stabling_geometry(geometry_id: int, db: Session = Depends(get_db)):
    db_geometry = crud.stabling.read_stabling_geometry(db, geometry_id=geometry_id)
    if db_geometry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stabling geometry not found"
        )
    return db_geometry

@router.put("/{geometry_id}", response_model=StablingGeometryResponse)
def update_stabling_geometry(geometry_id: int, geometry_data: StablingGeometryCreate, db: Session = Depends(get_db)):
    db_geometry = crud.stabling.read_stabling_geometry(db, geometry_id=geometry_id)
    if db_geometry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stabling geometry not found"
        )
    return crud.stabling.update_stabling_geometry(db=db, geometry_id=geometry_id, geometry_data=geometry_data.dict())

@router.delete("/{geometry_id}")
def delete_stabling_geometry(geometry_id: int, db: Session = Depends(get_db)):
    db_geometry = crud.stabling.read_stabling_geometry(db, geometry_id=geometry_id)
    if db_geometry is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stabling geometry not found"
        )
    crud.stabling.delete_stabling_geometry(db=db, geometry_id=geometry_id)
    return {"message": "Stabling geometry deleted successfully"}