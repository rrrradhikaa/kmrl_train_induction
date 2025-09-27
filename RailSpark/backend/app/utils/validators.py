import re
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
from sqlalchemy.orm import Session
import crud

class DateValidator:
    """Date validation utilities"""
    
    @staticmethod
    def is_valid_date(date_str: str, format: str = '%Y-%m-%d') -> bool:
        """Check if a date string is valid"""
        try:
            datetime.strptime(date_str, format)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_future_date(date_str: str, format: str = '%Y-%m-%d') -> bool:
        """Check if a date is in the future"""
        try:
            input_date = datetime.strptime(date_str, format).date()
            return input_date > datetime.now().date()
        except ValueError:
            return False
    
    @staticmethod
    def is_past_date(date_str: str, format: str = '%Y-%m-%d') -> bool:
        """Check if a date is in the past"""
        try:
            input_date = datetime.strptime(date_str, format).date()
            return input_date < datetime.now().date()
        except ValueError:
            return False
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str, format: str = '%Y-%m-%d') -> Tuple[bool, Optional[str]]:
        """Validate that start date is before end date"""
        try:
            start = datetime.strptime(start_date, format).date()
            end = datetime.strptime(end_date, format).date()
            
            if start > end:
                return False, "Start date cannot be after end date"
            
            return True, None
        except ValueError as e:
            return False, f"Invalid date format: {str(e)}"
    
    @staticmethod
    def is_within_range(date_str: str, start_range: str, end_range: str, format: str = '%Y-%m-%d') -> bool:
        """Check if a date is within a range"""
        try:
            check_date = datetime.strptime(date_str, format).date()
            start_date = datetime.strptime(start_range, format).date()
            end_date = datetime.strptime(end_range, format).date()
            
            return start_date <= check_date <= end_date
        except ValueError:
            return False

class FileValidator:
    """File validation utilities"""
    
    @staticmethod
    def validate_csv_structure(file_path: str, required_columns: List[str]) -> Tuple[bool, Optional[str]]:
        """Validate CSV file structure"""
        try:
            df = pd.read_csv(file_path)
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return False, f"Missing required columns: {', '.join(missing_columns)}"
            
            if df.empty:
                return False, "CSV file is empty"
            
            return True, None
        except Exception as e:
            return False, f"Error reading CSV file: {str(e)}"
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
        """Validate file extension"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def validate_file_size(file_path: str, max_size_mb: int = 10) -> Tuple[bool, Optional[str]]:
        """Validate file size"""
        try:
            file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
            if file_size_mb > max_size_mb:
                return False, f"File size {file_size_mb:.2f}MB exceeds maximum {max_size_mb}MB"
            return True, None
        except OSError as e:
            return False, f"Error checking file size: {str(e)}"

class DataValidator:
    """Main data validation class"""
    
    def __init__(self, db: Session):
        self.db = db
        self.date_validator = DateValidator()
        self.file_validator = FileValidator()
    
    def validate_train_data(self, train_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate train data"""
        errors = []
        
        # Validate train number format (e.g., KMRL-001)
        if not re.match(r'^[A-Z]{2,4}-\d{3}$', train_data.get('train_number', '')):
            errors.append("Train number must be in format: ABC-123")
        
        # Validate mileage
        mileage = train_data.get('current_mileage', 0)
        if not isinstance(mileage, int) or mileage < 0:
            errors.append("Mileage must be a positive integer")
        
        # Validate status
        valid_statuses = ['active', 'under_maintenance', 'retired']
        if train_data.get('status') not in valid_statuses:
            errors.append(f"Status must be one of: {', '.join(valid_statuses)}")
        
        # Validate maintenance date if provided
        if train_data.get('last_maintenance_date'):
            if not self.date_validator.is_valid_date(str(train_data['last_maintenance_date'])):
                errors.append("Invalid maintenance date format (use YYYY-MM-DD)")
        
        return len(errors) == 0, errors
    
    def validate_fitness_certificate(self, cert_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate fitness certificate data"""
        errors = []
        
        # Validate train exists
        train = crud.get_train(self.db, cert_data.get('train_id'))
        if not train:
            errors.append("Train ID does not exist")
        
        # Validate department
        valid_departments = ['Rolling-Stock', 'Signalling', 'Telecom']
        if cert_data.get('department') not in valid_departments:
            errors.append(f"Department must be one of: {', '.join(valid_departments)}")
        
        # Validate dates
        if not self.date_validator.is_valid_date(str(cert_data.get('valid_from', ''))):
            errors.append("Invalid valid_from date format (use YYYY-MM-DD)")
        
        if not self.date_validator.is_valid_date(str(cert_data.get('valid_until', ''))):
            errors.append("Invalid valid_until date format (use YYYY-MM-DD)")
        
        # Validate date range
        if cert_data.get('valid_from') and cert_data.get('valid_until'):
            is_valid, date_error = self.date_validator.validate_date_range(
                str(cert_data['valid_from']), str(cert_data['valid_until'])
            )
            if not is_valid:
                errors.append(date_error)
        
        return len(errors) == 0, errors
    
    def validate_job_card(self, job_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate job card data"""
        errors = []
        
        # Validate train exists
        train = crud.get_train(self.db, job_data.get('train_id'))
        if not train:
            errors.append("Train ID does not exist")
        
        # Validate work order ID format
        if not re.match(r'^WO-\w+$', job_data.get('work_order_id', '')):
            errors.append("Work order ID must be in format: WO-123ABC")
        
        # Validate status
        valid_statuses = ['open', 'closed']
        if job_data.get('status') not in valid_statuses:
            errors.append(f"Status must be one of: {', '.join(valid_statuses)}")
        
        return len(errors) == 0, errors
    
    def validate_branding_contract(self, contract_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate branding contract data"""
        errors = []
        
        # Validate train exists
        train = crud.get_train(self.db, contract_data.get('train_id'))
        if not train:
            errors.append("Train ID does not exist")
        
        # Validate exposure hours
        required_hours = contract_data.get('exposure_hours_required', 0)
        fulfilled_hours = contract_data.get('exposure_hours_fulfilled', 0)
        
        if not isinstance(required_hours, int) or required_hours <= 0:
            errors.append("Exposure hours required must be a positive integer")
        
        if not isinstance(fulfilled_hours, int) or fulfilled_hours < 0:
            errors.append("Exposure hours fulfilled must be a non-negative integer")
        
        if fulfilled_hours > required_hours:
            errors.append("Fulfilled hours cannot exceed required hours")
        
        # Validate dates
        if not self.date_validator.is_valid_date(str(contract_data.get('start_date', ''))):
            errors.append("Invalid start_date format (use YYYY-MM-DD)")
        
        if not self.date_validator.is_valid_date(str(contract_data.get('end_date', ''))):
            errors.append("Invalid end_date format (use YYYY-MM-DD)")
        
        # Validate date range
        if contract_data.get('start_date') and contract_data.get('end_date'):
            is_valid, date_error = self.date_validator.validate_date_range(
                str(contract_data['start_date']), str(contract_data['end_date'])
            )
            if not is_valid:
                errors.append(date_error)
        
        return len(errors) == 0, errors
    
    def validate_induction_plan(self, plan_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate induction plan data"""
        errors = []
        
        # Validate train exists
        train = crud.get_train(self.db, plan_data.get('train_id'))
        if not train:
            errors.append("Train ID does not exist")
        
        # Validate induction type
        valid_types = ['service', 'standby', 'maintenance']
        if plan_data.get('induction_type') not in valid_types:
            errors.append(f"Induction type must be one of: {', '.join(valid_types)}")
        
        # Validate rank
        rank = plan_data.get('rank', 0)
        if not isinstance(rank, int) or rank <= 0:
            errors.append("Rank must be a positive integer")
        
        # Validate date
        if not self.date_validator.is_valid_date(str(plan_data.get('plan_date', ''))):
            errors.append("Invalid plan date format (use YYYY-MM-DD)")
        
        return len(errors) == 0, errors
    
    def validate_whatsapp_message(self, message: str) -> Tuple[bool, List[str]]:
        """Validate WhatsApp message format"""
        errors = []
        
        if not message or len(message.strip()) == 0:
            errors.append("Message cannot be empty")
        
        if len(message) > 500:
            errors.append("Message too long (max 500 characters)")
        
        # Check for required keywords based on message type
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['train', 'maintenance', 'fitness', 'cleaning']):
            # Check if message has basic structure
            if ':' not in message and 'for' not in message:
                errors.append("Message should contain structured information (use ':' or 'for')")
        
        return len(errors) == 0, errors
    
    def validate_csv_upload(self, file_path: str, data_type: str) -> Tuple[bool, List[str]]:
        """Validate CSV upload based on data type"""
        errors = []
        
        # Define required columns for each data type
        required_columns = {
            'trains': ['train_number', 'current_mileage', 'status'],
            'fitness': ['train_number', 'department', 'valid_from', 'valid_until'],
            'job_cards': ['train_number', 'work_order_id', 'status'],
            'branding': ['train_number', 'advertiser_name', 'exposure_hours_required', 'start_date', 'end_date']
        }
        
        if data_type not in required_columns:
            errors.append(f"Unknown data type: {data_type}")
            return False, errors
        
        # Validate file structure
        is_valid, error_msg = self.file_validator.validate_csv_structure(file_path, required_columns[data_type])
        if not is_valid:
            errors.append(error_msg)
        
        return len(errors) == 0, errors

# Import os for file size validation
import os