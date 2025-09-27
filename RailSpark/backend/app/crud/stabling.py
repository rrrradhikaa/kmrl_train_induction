from sqlalchemy.orm import Session
from models import StablingGeometry
from schemas import StablingGeometryCreate
from typing import List, Optional

def read_stabling_geometry(db: Session, geometry_id: int) -> Optional[StablingGeometry]:
    return db.query(StablingGeometry).filter(StablingGeometry.id == geometry_id).first()

def read_stabling_geometries(db: Session, skip: int = 0, limit: int = 100) -> List[StablingGeometry]:
    return db.query(StablingGeometry).offset(skip).limit(limit).all()

def read_geometry_by_train(db: Session, train_id: int) -> Optional[StablingGeometry]:
    return db.query(StablingGeometry).filter(StablingGeometry.train_id == train_id).order_by(StablingGeometry.stabled_at.desc()).first()

def read_trains_in_bay(db: Session, bay_position: str) -> List[StablingGeometry]:
    return db.query(StablingGeometry).filter(StablingGeometry.bay_position == bay_position).all()

def read_bays_requiring_shunting(db: Session) -> List[StablingGeometry]:
    return db.query(StablingGeometry).filter(StablingGeometry.shunting_required == True).all()

def create_stabling_geometry(db: Session, geometry: StablingGeometryCreate) -> StablingGeometry:
    db_geometry = StablingGeometry(
        train_id=geometry.train_id,
        bay_position=geometry.bay_position,
        shunting_required=geometry.shunting_required
    )
    db.add(db_geometry)
    db.commit()
    db.refresh(db_geometry)
    return db_geometry

def update_stabling_geometry(db: Session, geometry_id: int, geometry_data: dict) -> Optional[StablingGeometry]:
    db_geometry = db.query(StablingGeometry).filter(StablingGeometry.id == geometry_id).first()
    if db_geometry:
        for key, value in geometry_data.items():
            setattr(db_geometry, key, value)
        db.commit()
        db.refresh(db_geometry)
    return db_geometry

def delete_stabling_geometry(db: Session, geometry_id: int) -> bool:
    db_geometry = db.query(StablingGeometry).filter(StablingGeometry.id == geometry_id).first()
    if db_geometry:
        db.delete(db_geometry)
        db.commit()
        return True
    return False

def optimize_stabling_arrangement(db: Session) -> List[StablingGeometry]:
    """Simple optimization to minimize shunting"""
    # This would be enhanced with actual optimization logic
    current_arrangements = read_stabling_geometries(db)
    # Basic logic: mark arrangements that need shunting
    for arrangement in current_arrangements:
        # Simple rule: if train is not in optimal position, mark for shunting
        optimal_position = f"Bay-{arrangement.train_id % 10 + 1}"  # Example logic
        if arrangement.bay_position != optimal_position:
            arrangement.shunting_required = True
        else:
            arrangement.shunting_required = False
    db.commit()
    return current_arrangements