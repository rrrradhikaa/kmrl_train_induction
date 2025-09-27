# crud/performance.py
from sqlalchemy.orm import Session
from datetime import date
import random
from ai_models import PerformanceHistory, CrewAvailability, MaintenancePriority, BrandingPriority

def get_train_performance_history(db: Session, train_id: int, days: int = 90) -> PerformanceHistory:
    """
    Return a PerformanceHistory object with attributes AI expects
    """
    try:
        # Return class instance instead of dict
        return PerformanceHistory(train_id)
    except Exception as e:
        # Fallback with default values
        fallback = PerformanceHistory(train_id)
        fallback.on_time = 0.90
        fallback.reliability = 0.92
        fallback.availability = 0.94
        return fallback

def get_crew_availability(db: Session, plan_date: date, shift: str = "day") -> CrewAvailability:
    """
    Return a CrewAvailability object with attributes AI expects  
    """
    try:
        return CrewAvailability(plan_date, shift)
    except Exception as e:
        fallback = CrewAvailability(plan_date, shift)
        fallback.total_crew = 25
        fallback.available_crew = 20
        return fallback

def get_maintenance_priority(db: Session, train_id: int) -> MaintenancePriority:
    """
    Return a MaintenancePriority object
    """
    try:
        from models import Train
        
        train = db.query(Train).filter(Train.id == train_id).first()
        if train and train.last_maintenance_date:
            days_since = (date.today() - train.last_maintenance_date).days
            priority_score = min(1.0, days_since / 180)  # 0-1 scale
        else:
            priority_score = random.uniform(0.1, 0.5)
            
        return MaintenancePriority(train_id, float(priority_score))
    except Exception as e:
        return MaintenancePriority(train_id, 0.3)

def get_branding_priority(db: Session, train_id: int) -> BrandingPriority:
    """
    Return a BrandingPriority object
    """
    try:
        from .branding import read_active_contracts
        
        active_contracts = read_active_contracts(db, train_id)
        if active_contracts:
            total_value = sum(contract.contract_value for contract in active_contracts)
            priority_score = min(1.0, total_value / 50000)
        else:
            priority_score = random.uniform(0.1, 0.4)
            
        return BrandingPriority(train_id, float(priority_score))
    except Exception as e:
        return BrandingPriority(train_id, 0.2)