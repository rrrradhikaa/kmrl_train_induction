from sqlalchemy.orm import Session
from models import InductionPlan
from schemas import InductionPlanCreate
from typing import List, Optional
from datetime import date, datetime

def read_induction_plan(db: Session, plan_id: int) -> Optional[InductionPlan]:
    return db.query(InductionPlan).filter(InductionPlan.id == plan_id).first()

def read_induction_plans(db: Session, skip: int = 0, limit: int = 100) -> List[InductionPlan]:
    return db.query(InductionPlan).offset(skip).limit(limit).all()

def read_plans_by_date(db: Session, plan_date: date) -> List[InductionPlan]:
    return db.query(InductionPlan).filter(InductionPlan.plan_date == plan_date).order_by(InductionPlan.rank).all()

def read_plans_by_train(db: Session, train_id: int) -> List[InductionPlan]:
    return db.query(InductionPlan).filter(InductionPlan.train_id == train_id).order_by(InductionPlan.plan_date.desc()).all()

def read_todays_plan(db: Session) -> List[InductionPlan]:
    today = date.today()
    return read_plans_by_date(db, today)

def create_induction_plan(db: Session, plan: InductionPlanCreate) -> InductionPlan:
    db_plan = InductionPlan(
        plan_date=plan.plan_date,
        train_id=plan.train_id,
        induction_type=plan.induction_type,
        rank=plan.rank,
        reason=plan.reason
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def create_bulk_induction_plans(db: Session, plans: List[InductionPlanCreate]) -> List[InductionPlan]:
    """Create multiple induction plans at once"""
    db_plans = []
    for plan in plans:
        db_plan = InductionPlan(
            plan_date=plan.plan_date,
            train_id=plan.train_id,
            induction_type=plan.induction_type,
            rank=plan.rank,
            reason=plan.reason
        )
        db.add(db_plan)
        db_plans.append(db_plan)
    db.commit()
    for plan in db_plans:
        db.refresh(plan)
    return db_plans

def update_induction_plan(db: Session, plan_id: int, plan_data: dict) -> Optional[InductionPlan]:
    db_plan = db.query(InductionPlan).filter(InductionPlan.id == plan_id).first()
    if db_plan:
        for key, value in plan_data.items():
            setattr(db_plan, key, value)
        db.commit()
        db.refresh(db_plan)
    return db_plan

def delete_induction_plan(db: Session, plan_id: int) -> bool:
    db_plan = db.query(InductionPlan).filter(InductionPlan.id == plan_id).first()
    if db_plan:
        db.delete(db_plan)
        db.commit()
        return True
    return False

def approve_induction_plan(db: Session, plan_id: int, approved_by: int) -> Optional[InductionPlan]:
    return update_induction_plan(db, plan_id, {
        "approved_by": approved_by,
        "approved_at": datetime.now()
    })

def read_service_trains_for_date(db: Session, plan_date: date) -> List[InductionPlan]:
    """Get trains scheduled for service on a specific date"""
    return db.query(InductionPlan).filter(
        InductionPlan.plan_date == plan_date,
        InductionPlan.induction_type == "service"
    ).order_by(InductionPlan.rank).all()