from sqlalchemy.orm import Session
from models import FitnessCertificate
from schemas import FitnessCertificateCreate
from typing import List, Optional
from datetime import date

def read_fitness_certificate(db: Session, cert_id: int) -> Optional[FitnessCertificate]:
    return db.query(FitnessCertificate).filter(FitnessCertificate.id == cert_id).first()

def read_fitness_certificates(db: Session, skip: int = 0, limit: int = 100) -> List[FitnessCertificate]:
    return db.query(FitnessCertificate).offset(skip).limit(limit).all()

def read_certificates_by_train(db: Session, train_id: int) -> List[FitnessCertificate]:
    return db.query(FitnessCertificate).filter(FitnessCertificate.train_id == train_id).all()

def read_valid_certificates(db: Session, train_id: int) -> List[FitnessCertificate]:
    today = date.today()
    return db.query(FitnessCertificate).filter(
        FitnessCertificate.train_id == train_id,
        FitnessCertificate.valid_from <= today,
        FitnessCertificate.valid_until >= today,
        FitnessCertificate.is_valid == True
    ).all()

def create_fitness_certificate(db: Session, cert: FitnessCertificateCreate) -> FitnessCertificate:
    db_cert = FitnessCertificate(
        train_id=cert.train_id,
        department=cert.department,
        valid_from=cert.valid_from,
        valid_until=cert.valid_until,
        is_valid=cert.is_valid
    )
    db.add(db_cert)
    db.commit()
    db.refresh(db_cert)
    return db_cert

def update_fitness_certificate(db: Session, cert_id: int, cert_data: dict) -> Optional[FitnessCertificate]:
    db_cert = db.query(FitnessCertificate).filter(FitnessCertificate.id == cert_id).first()
    if db_cert:
        for key, value in cert_data.items():
            setattr(db_cert, key, value)
        db.commit()
        db.refresh(db_cert)
    return db_cert

def delete_fitness_certificate(db: Session, cert_id: int) -> bool:
    db_cert = db.query(FitnessCertificate).filter(FitnessCertificate.id == cert_id).first()
    if db_cert:
        db.delete(db_cert)
        db.commit()
        return True
    return False

def check_train_fitness_for_service(db: Session, train_id: int) -> bool:
    """Check if train has all required valid certificates"""
    required_departments = ["Rolling-Stock", "Signalling", "Telecom"]
    valid_certs = read_valid_certificates(db, train_id)
    cert_departments = {cert.department for cert in valid_certs}
    return all(dept in cert_departments for dept in required_departments)