from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import tempfile
import os
from database import get_db
from utils.data_loader import DataLoader
from utils.validators import DataValidator
import schemas
import crud

router = APIRouter(prefix="/upload", tags=["data upload"])

@router.post("/whatsapp")
def upload_whatsapp_messages(
    messages: schemas.WhatsAppUpload,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Upload and process WhatsApp messages"""
    data_loader = DataLoader(db)
    validator = DataValidator(db)
    
    # Validate messages
    validation_errors = []
    for message in messages.messages:
        is_valid, errors = validator.validate_whatsapp_message(message)
        if not is_valid:
            validation_errors.extend(errors)
    
    if validation_errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"validation_errors": validation_errors}
        )
    
    # Process messages
    try:
        results = data_loader.process_whatsapp_updates(messages.messages)
        
        return {
            "success": True,
            "messages_processed": results["messages_processed"],
            "updates_applied": results["updates_applied"],
            "errors": results["errors"],
            "validation_errors": validation_errors
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing WhatsApp messages: {str(e)}"
        )

@router.post("/csv")
async def upload_csv_file(
    data_type: str = Form(..., description="Type of data: trains, fitness, job_cards, branding"),
    file: UploadFile = File(..., description="CSV file to upload"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Upload and process CSV file"""
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are supported"
        )
    
    data_loader = DataLoader(db)
    validator = DataValidator(db)
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name
    
    try:
        # Validate CSV structure
        is_valid, errors = validator.validate_csv_upload(temp_file_path, data_type)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"validation_errors": errors}
            )
        
        # Load data from CSV
        load_result = data_loader.load_csv_file(temp_file_path, data_type)
        if not load_result['success']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=load_result['error']
            )
        
        # Prepare data for database
        data_to_save = {f"{data_type}": load_result['data']}
        
        # Save to database
        save_result = data_loader.save_to_database(data_to_save)
        
        return {
            "success": True,
            "data_type": data_type,
            "records_loaded": load_result['records_loaded'],
            "database_results": save_result,
            "file_name": file.filename
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing CSV file: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@router.post("/manual")
def upload_manual_data(
    data: schemas.ManualDataUpload,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Upload data manually via API"""
    data_loader = DataLoader(db)
    validator = DataValidator(db)
    
    results = {
        "trains_processed": 0,
        "fitness_certs_processed": 0,
        "job_cards_processed": 0,
        "branding_contracts_processed": 0,
        "errors": []
    }
    
    # Process trains data
    if data.trains:
        for train_data in data.trains:
            try:
                is_valid, errors = validator.validate_train_data(train_data)
                if is_valid:
                    # Check if train exists
                    existing_train = crud.trains.read_train_by_number(db, train_data.train_number)
                    if not existing_train:
                        crud.trains.create_train(db, train_data)
                        results["trains_processed"] += 1
                else:
                    results["errors"].append(f"Train {train_data.train_number}: {', '.join(errors)}")
            except Exception as e:
                results["errors"].append(f"Train {train_data.train_number}: {str(e)}")
    
    # Process fitness certificates
    if data.fitness_certificates:
        for cert_data in data.fitness_certificates:
            try:
                is_valid, errors = validator.validate_fitness_certificate(cert_data)
                if is_valid:
                    crud.fitness.create_fitness_certificate(db, cert_data)
                    results["fitness_certs_processed"] += 1
                else:
                    results["errors"].append(f"Fitness cert for train {cert_data.train_id}: {', '.join(errors)}")
            except Exception as e:
                results["errors"].append(f"Fitness cert for train {cert_data.train_id}: {str(e)}")
    
    # Process job cards
    if data.job_cards:
        for job_data in data.job_cards:
            try:
                is_valid, errors = validator.validate_job_card(job_data)
                if is_valid:
                    crud.job_cards.create_job_card(db, job_data)
                    results["job_cards_processed"] += 1
                else:
                    results["errors"].append(f"Job card {job_data.work_order_id}: {', '.join(errors)}")
            except Exception as e:
                results["errors"].append(f"Job card {job_data.work_order_id}: {str(e)}")
    
    # Process branding contracts
    if data.branding_contracts:
        for contract_data in data.branding_contracts:
            try:
                is_valid, errors = validator.validate_branding_contract(contract_data)
                if is_valid:
                    crud.branding.create_branding_contract(db, contract_data)
                    results["branding_contracts_processed"] += 1
                else:
                    results["errors"].append(f"Branding contract for train {contract_data.train_id}: {', '.join(errors)}")
            except Exception as e:
                results["errors"].append(f"Branding contract for train {contract_data.train_id}: {str(e)}")
    
    return results

@router.get("/templates/{data_type}")
def download_csv_template(data_type: str):
    """Download CSV template for data upload"""
    templates = {
        "trains": "train_number,current_mileage,last_maintenance_date,status\nKMRL-001,15000,2024-01-15,active\nKMRL-002,12000,2024-01-10,active",
        "fitness": "train_number,department,valid_from,valid_until,is_valid\nKMRL-001,Rolling-Stock,2024-01-01,2024-12-31,true\nKMRL-001,Signalling,2024-01-01,2024-12-31,true",
        "job_cards": "train_number,work_order_id,status,description\nKMRL-001,WO-123,open,Brake inspection\nKMRL-002,WO-124,closed,AC repair",
        "branding": "train_number,advertiser_name,exposure_hours_required,exposure_hours_fulfilled,start_date,end_date\nKMRL-001,Coca-Cola,160,80,2024-01-01,2024-06-30\nKMRL-002,Pepsi,200,120,2024-01-01,2024-06-30"
    }
    
    if data_type not in templates:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Template not available for data type: {data_type}"
        )
    
    return {
        "data_type": data_type,
        "template": templates[data_type],
        "filename": f"{data_type}_template.csv"
    }