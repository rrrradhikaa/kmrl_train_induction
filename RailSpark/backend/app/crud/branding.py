from sqlalchemy.orm import Session
from models import BrandingContract
from schemas import BrandingContractCreate
from typing import List, Optional
from datetime import date

def read_branding_contract(db: Session, contract_id: int) -> Optional[BrandingContract]:
    return db.query(BrandingContract).filter(BrandingContract.id == contract_id).first()

def read_branding_contracts(db: Session, skip: int = 0, limit: int = 100) -> List[BrandingContract]:
    return db.query(BrandingContract).offset(skip).limit(limit).all()

def read_contracts_by_train(db: Session, train_id: int) -> List[BrandingContract]:
    return db.query(BrandingContract).filter(BrandingContract.train_id == train_id).all()

def read_active_contracts(db: Session, train_id: int = None) -> List[BrandingContract]:
    today = date.today()
    query = db.query(BrandingContract).filter(
        BrandingContract.start_date <= today,
        BrandingContract.end_date >= today
    )
    if train_id:
        query = query.filter(BrandingContract.train_id == train_id)
    return query.all()

def create_branding_contract(db: Session, contract: BrandingContractCreate) -> BrandingContract:
    db_contract = BrandingContract(
        train_id=contract.train_id,
        advertiser_name=contract.advertiser_name,
        exposure_hours_required=contract.exposure_hours_required,
        exposure_hours_fulfilled=contract.exposure_hours_fulfilled,
        start_date=contract.start_date,
        end_date=contract.end_date
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

def update_branding_contract(db: Session, contract_id: int, contract_data: dict) -> Optional[BrandingContract]:
    db_contract = db.query(BrandingContract).filter(BrandingContract.id == contract_id).first()
    if db_contract:
        for key, value in contract_data.items():
            setattr(db_contract, key, value)
        db.commit()
        db.refresh(db_contract)
    return db_contract

def delete_branding_contract(db: Session, contract_id: int) -> bool:
    db_contract = db.query(BrandingContract).filter(BrandingContract.id == contract_id).first()
    if db_contract:
        db.delete(db_contract)
        db.commit()
        return True
    return False

def update_exposure_hours(db: Session, contract_id: int, hours: int) -> Optional[BrandingContract]:
    db_contract = db.query(BrandingContract).filter(BrandingContract.id == contract_id).first()
    if db_contract:
        db_contract.exposure_hours_fulfilled += hours
        db.commit()
        db.refresh(db_contract)
    return db_contract

def read_contracts_need_exposure(db: Session) -> List[BrandingContract]:
    """Get contracts that need more exposure hours"""
    active_contracts = read_active_contracts(db)
    return [contract for contract in active_contracts 
            if contract.exposure_hours_fulfilled < contract.exposure_hours_required]