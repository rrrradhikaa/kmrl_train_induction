from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import BrandingContractCreate, BrandingContractResponse
import crud

router = APIRouter(prefix="/branding", tags=["branding contracts"])

@router.post("/", response_model=BrandingContractResponse, status_code=status.HTTP_201_CREATED)
def create_branding_contract(contract: BrandingContractCreate, db: Session = Depends(get_db)):
    # Verify train exists
    db_train = crud.trains.read_train(db, train_id=contract.train_id)
    if not db_train:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Train not found"
        )
    return crud.branding.create_branding_contract(db=db, contract=contract)

@router.get("/", response_model=List[BrandingContractResponse])
def read_branding_contracts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contracts = crud.branding.read_branding_contracts(db, skip=skip, limit=limit)
    return contracts

@router.get("/train/{train_id}", response_model=List[BrandingContractResponse])
def read_contracts_by_train(train_id: int, db: Session = Depends(get_db)):
    contracts = crud.branding.read_contracts_by_train(db, train_id=train_id)
    return contracts

@router.get("/active", response_model=List[BrandingContractResponse])
def read_active_contracts(train_id: int = None, db: Session = Depends(get_db)):
    contracts = crud.branding.read_active_contracts(db, train_id=train_id)
    return contracts

@router.get("/need-exposure", response_model=List[BrandingContractResponse])
def read_contracts_need_exposure(db: Session = Depends(get_db)):
    contracts = crud.branding.read_contracts_need_exposure(db)
    return contracts

@router.get("/{contract_id}", response_model=BrandingContractResponse)
def read_branding_contract(contract_id: int, db: Session = Depends(get_db)):
    db_contract = crud.branding.read_branding_contract(db, contract_id=contract_id)
    if db_contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branding contract not found"
        )
    return db_contract

@router.put("/{contract_id}", response_model=BrandingContractResponse)
def update_branding_contract(contract_id: int, contract_data: BrandingContractCreate, db: Session = Depends(get_db)):
    db_contract = crud.branding.read_branding_contract(db, contract_id=contract_id)
    if db_contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branding contract not found"
        )
    return crud.branding.update_branding_contract(db=db, contract_id=contract_id, contract_data=contract_data.dict())

@router.patch("/{contract_id}/exposure")
def update_exposure_hours(contract_id: int, hours: int, db: Session = Depends(get_db)):
    db_contract = crud.branding.read_branding_contract(db, contract_id=contract_id)
    if db_contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branding contract not found"
        )
    updated_contract = crud.branding.update_exposure_hours(db=db, contract_id=contract_id, hours=hours)
    return {
        "message": f"Exposure hours updated successfully. Current: {updated_contract.exposure_hours_fulfilled}/{updated_contract.exposure_hours_required}"
    }

@router.delete("/{contract_id}")
def delete_branding_contract(contract_id: int, db: Session = Depends(get_db)):
    db_contract = crud.branding.read_branding_contract(db, contract_id=contract_id)
    if db_contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branding contract not found"
        )
    crud.branding.delete_branding_contract(db=db, contract_id=contract_id)
    return {"message": "Branding contract deleted successfully"}