from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import FitnessCertificateCreate, FitnessCertificateResponse
import crud

router = APIRouter(prefix="/fitness", tags=["fitness certificates"])

@router.post("/", response_model=FitnessCertificateResponse, status_code=status.HTTP_201_CREATED)
def create_fitness_certificate(cert: FitnessCertificateCreate, db: Session = Depends(get_db)):
    # Verify train exists
    db_train = crud.trains.read_train(db, train_id=cert.train_id)
    if not db_train:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Train not found"
        )
    return crud.fitness.create_fitness_certificate(db=db, cert=cert)

@router.get("/", response_model=List[FitnessCertificateResponse])
def read_fitness_certificates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    certificates = crud.fitness.read_fitness_certificates(db, skip=skip, limit=limit)
    return certificates

@router.get("/train/{train_id}", response_model=List[FitnessCertificateResponse])
def read_certificates_by_train(train_id: int, db: Session = Depends(get_db)):
    certificates = crud.fitness.read_certificates_by_train(db, train_id=train_id)
    return certificates

@router.get("/train/{train_id}/valid", response_model=List[FitnessCertificateResponse])
def read_valid_certificates(train_id: int, db: Session = Depends(get_db)):
    certificates = crud.fitness.read_valid_certificates(db, train_id=train_id)
    return certificates

@router.get("/train/{train_id}/service-check")
def check_train_fitness_for_service(train_id: int, db: Session = Depends(get_db)):
    is_fit = crud.fitness.check_train_fitness_for_service(db, train_id=train_id)
    return {
        "train_id": train_id,
        "fit_for_service": is_fit,
        "message": "Train is fit for service" if is_fit else "Train is not fit for service"
    }

@router.get("/{cert_id}", response_model=FitnessCertificateResponse)
def read_fitness_certificate(cert_id: int, db: Session = Depends(get_db)):
    db_cert = crud.fitness.read_fitness_certificate(db, cert_id=cert_id)
    if db_cert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitness certificate not found"
        )
    return db_cert

@router.put("/{cert_id}", response_model=FitnessCertificateResponse)
def update_fitness_certificate(cert_id: int, cert_data: FitnessCertificateCreate, db: Session = Depends(get_db)):
    db_cert = crud.fitness.read_fitness_certificate(db, cert_id=cert_id)
    if db_cert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitness certificate not found"
        )
    return crud.fitness.update_fitness_certificate(db=db, cert_id=cert_id, cert_data=cert_data.dict())

@router.delete("/{cert_id}")
def delete_fitness_certificate(cert_id: int, db: Session = Depends(get_db)):
    db_cert = crud.fitness.read_fitness_certificate(db, cert_id=cert_id)
    if db_cert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fitness certificate not found"
        )
    crud.fitness.delete_fitness_certificate(db=db, cert_id=cert_id)
    return {"message": "Fitness certificate deleted successfully"}