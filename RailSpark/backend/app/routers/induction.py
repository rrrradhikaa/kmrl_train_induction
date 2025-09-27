from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from database import get_db
from schemas import InductionPlanCreate, InductionPlanResponse
import crud

router = APIRouter(prefix="/induction", tags=["induction plans"])

@router.post("/", response_model=InductionPlanResponse, status_code=status.HTTP_201_CREATED)
def create_induction_plan(plan: InductionPlanCreate, db: Session = Depends(get_db)):
    # Verify train exists
    db_train = crud.trains.read_train(db, train_id=plan.train_id)
    if not db_train:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Train not found"
        )
    return crud.induction.create_induction_plan(db=db, plan=plan)

@router.post("/bulk", response_model=List[InductionPlanResponse], status_code=status.HTTP_201_CREATED)
def create_bulk_induction_plans(plans: List[InductionPlanCreate], db: Session = Depends(get_db)):
    # Verify all trains exist
    for plan in plans:
        db_train = crud.trains.read_train(db, train_id=plan.train_id)
        if not db_train:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Train {plan.train_id} not found"
            )
    return crud.induction.create_bulk_induction_plans(db=db, plans=plans)

@router.get("/", response_model=List[InductionPlanResponse])
def read_induction_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plans = crud.induction.read_induction_plans(db, skip=skip, limit=limit)
    return plans

@router.get("/date/{plan_date}", response_model=List[InductionPlanResponse])
def read_plans_by_date(plan_date: date, db: Session = Depends(get_db)):
    plans = crud.induction.read_plans_by_date(db, plan_date=plan_date)
    return plans

@router.get("/train/{train_id}", response_model=List[InductionPlanResponse])
def read_plans_by_train(train_id: int, db: Session = Depends(get_db)):
    plans = crud.induction.read_plans_by_train(db, train_id=train_id)
    return plans

@router.get("/today", response_model=List[InductionPlanResponse])
def read_todays_plan(db: Session = Depends(get_db)):
    plans = crud.induction.read_todays_plan(db)
    return plans

@router.get("/service-trains/{plan_date}", response_model=List[InductionPlanResponse])
def read_service_trains_for_date(plan_date: date, db: Session = Depends(get_db)):
    plans = crud.induction.read_service_trains_for_date(db, plan_date=plan_date)
    return plans

@router.get("/{plan_id}", response_model=InductionPlanResponse)
def read_induction_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = crud.induction.read_induction_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Induction plan not found"
        )
    return db_plan

@router.put("/{plan_id}", response_model=InductionPlanResponse)
def update_induction_plan(plan_id: int, plan_data: InductionPlanCreate, db: Session = Depends(get_db)):
    db_plan = crud.induction.read_induction_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Induction plan not found"
        )
    return crud.induction.update_induction_plan(db=db, plan_id=plan_id, plan_data=plan_data.dict())

@router.post("/{plan_id}/approve", response_model=InductionPlanResponse)
def approve_induction_plan(plan_id: int, approved_by: int, db: Session = Depends(get_db)):
    db_plan = crud.induction.read_induction_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Induction plan not found"
        )
    return crud.induction.approve_induction_plan(db=db, plan_id=plan_id, approved_by=approved_by)

@router.delete("/{plan_id}")
def delete_induction_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = crud.induction.read_induction_plan(db, plan_id=plan_id)
    if db_plan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Induction plan not found"
        )
    crud.induction.delete_induction_plan(db=db, plan_id=plan_id)
    return {"message": "Induction plan deleted successfully"}