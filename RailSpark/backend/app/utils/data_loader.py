import pandas as pd
import csv
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, date
from sqlalchemy.orm import Session
import re
import crud
import schemas  # Add this import
from models import Train, FitnessCertificate, JobCard, BrandingContract, CleaningSlot, StablingGeometry

class WhatsAppParser:
    """Parser for WhatsApp message format data"""
    
    @staticmethod
    def parse_message(message: str) -> Dict[str, Any]:
        """Parse a WhatsApp message into structured data"""
        try:
            data = {}
            
            # Common WhatsApp message patterns
            if "train" in message.lower() and "status" in message.lower():
                data['type'] = 'train_status'
                data.update(WhatsAppParser._parse_train_status(message))
            
            elif "maintenance" in message.lower() or "job card" in message.lower():
                data['type'] = 'maintenance_update'
                data.update(WhatsAppParser._parse_maintenance(message))
            
            elif "fitness" in message.lower() or "certificate" in message.lower():
                data['type'] = 'fitness_update'
                data.update(WhatsAppParser._parse_fitness(message))
            
            elif "cleaning" in message.lower() or "bay" in message.lower():
                data['type'] = 'cleaning_schedule'
                data.update(WhatsAppParser._parse_cleaning(message))
            
            else:
                data['type'] = 'general_update'
                data['raw_message'] = message
                data['timestamp'] = datetime.now()
            
            return data
            
        except Exception as e:
            return {'type': 'error', 'error': str(e), 'raw_message': message}
    
    @staticmethod
    def _parse_train_status(message: str) -> Dict[str, Any]:
        """Parse train status messages"""
        # Example: "Train KMRL-001 status: active, mileage: 15000"
        patterns = {
            'train_number': r'Train\s+([A-Z0-9-]+)',
            'status': r'status:\s*(\w+)',
            'mileage': r'mileage:\s*(\d+)'
        }
        
        result = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                result[key] = match.group(1)
        
        return result
    
    @staticmethod
    def _parse_maintenance(message: str) -> Dict[str, Any]:
        """Parse maintenance update messages"""
        # Example: "Job card WO-123 for KMRL-002: open, description: brake repair"
        patterns = {
            'work_order_id': r'WO-(\w+)',
            'train_number': r'for\s+([A-Z0-9-]+)',
            'status': r'status:\s*(\w+)',
            'description': r'description:\s*([^.,]+)'
        }
        
        result = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                result[key] = match.group(1)
        
        return result
    
    @staticmethod
    def _parse_fitness(message: str) -> Dict[str, Any]:
        """Parse fitness certificate messages"""
        # Example: "Fitness certificate for KMRL-003: Rolling-Stock, valid until 2024-12-31"
        patterns = {
            'train_number': r'for\s+([A-Z0-9-]+)',
            'department': r'([A-Za-z-]+),',
            'valid_until': r'valid until\s*(\d{4}-\d{2}-\d{2})'
        }
        
        result = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                result[key] = match.group(1)
        
        return result
    
    @staticmethod
    def _parse_cleaning(message: str) -> Dict[str, Any]:
        """Parse cleaning schedule messages"""
        # Example: "Cleaning scheduled for KMRL-004 at Bay 3, 2024-01-15 14:00"
        patterns = {
            'train_number': r'for\s+([A-Z0-9-]+)',
            'bay_number': r'Bay\s*(\d+)',
            'datetime': r'at\s*(\d{4}-\d{2}-\d{2}\s*\d{1,2}:\d{2})'
        }
        
        result = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                result[key] = match.group(1)
        
        return result

class CSVLoader:
    """Loader for CSV file data"""
    
    @staticmethod
    def load_trains_csv(file_path: str) -> List[Dict[str, Any]]:
        """Load trains data from CSV"""
        df = pd.read_csv(file_path)
        data = []
        
        for _, row in df.iterrows():
            # Handle NaN values and ensure proper data types
            train_number = str(row.get('train_number', '')).strip()
            if not train_number or train_number.lower() == 'nan':
                continue  # Skip rows without train number
                
            train_data = {
                'train_number': train_number,
                'current_mileage': CSVLoader._safe_int(row.get('current_mileage')),
                'last_maintenance_date': CSVLoader._parse_date(row.get('last_maintenance_date')),
                'status': str(row.get('status', 'active')).lower()
            }
            
            # Add optional fields if they exist in CSV
            optional_fields = ['train_name', 'capacity', 'model', 'coaches', 'max_speed']
            for field in optional_fields:
                if field in row and not pd.isna(row[field]):
                    if field in ['capacity', 'coaches', 'max_speed']:
                        train_data[field] = CSVLoader._safe_int(row[field])
                    else:
                        train_data[field] = str(row[field]).strip()
            
            data.append(train_data)
        
        return data
    
    @staticmethod
    def load_fitness_csv(file_path: str) -> List[Dict[str, Any]]:
        """Load fitness certificates from CSV"""
        df = pd.read_csv(file_path)
        data = []
        
        for _, row in df.iterrows():
            train_number = str(row.get('train_number', '')).strip()
            if not train_number or train_number.lower() == 'nan':
                continue
                
            cert_data = {
                'train_number': train_number,
                'department': str(row.get('department', '')).strip(),
                'valid_from': CSVLoader._parse_date(row.get('valid_from')),
                'valid_until': CSVLoader._parse_date(row.get('valid_until')),
                'is_valid': CSVLoader._safe_bool(row.get('is_valid', True))
            }
            data.append(cert_data)
        
        return data
    
    @staticmethod
    def load_job_cards_csv(file_path: str) -> List[Dict[str, Any]]:
        """Load job cards from CSV"""
        df = pd.read_csv(file_path)
        data = []
        
        for _, row in df.iterrows():
            train_number = str(row.get('train_number', '')).strip()
            if not train_number or train_number.lower() == 'nan':
                continue
                
            job_data = {
                'train_number': train_number,
                'work_order_id': str(row.get('work_order_id', '')).strip(),
                'status': str(row.get('status', 'open')).lower(),
                'description': str(row.get('description', ''))
            }
            
            # Add optional fields
            optional_fields = ['scheduled_date', 'completed_date', 'estimated_hours']
            for field in optional_fields:
                if field in row and not pd.isna(row[field]):
                    if field in ['estimated_hours']:
                        job_data[field] = CSVLoader._safe_int(row[field])
                    elif field in ['scheduled_date', 'completed_date']:
                        job_data[field] = CSVLoader._parse_date(row[field])
                    else:
                        job_data[field] = str(row[field]).strip()
            
            data.append(job_data)
        
        return data
    
    @staticmethod
    def load_branding_csv(file_path: str) -> List[Dict[str, Any]]:
        """Load branding contracts from CSV"""
        df = pd.read_csv(file_path)
        data = []
        
        for _, row in df.iterrows():
            train_number = str(row.get('train_number', '')).strip()
            if not train_number or train_number.lower() == 'nan':
                continue
                
            contract_data = {
                'train_number': train_number,
                'advertiser_name': str(row.get('advertiser_name', '')),
                'exposure_hours_required': CSVLoader._safe_int(row.get('exposure_hours_required', 0)),
                'exposure_hours_fulfilled': CSVLoader._safe_int(row.get('exposure_hours_fulfilled', 0)),
                'start_date': CSVLoader._parse_date(row.get('start_date')),
                'end_date': CSVLoader._parse_date(row.get('end_date'))
            }
            data.append(contract_data)
        
        return data
    
    @staticmethod
    def _parse_date(date_str: Any) -> Optional[date]:
        """Parse date string to date object"""
        if pd.isna(date_str) or not date_str:
            return None
        
        try:
            if isinstance(date_str, str):
                # Try different date formats
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y.%m.%d']:
                    try:
                        return datetime.strptime(date_str, fmt).date()
                    except ValueError:
                        continue
            elif isinstance(date_str, datetime):
                return date_str.date()
        except (ValueError, TypeError):
            return None
        
        return None
    
    @staticmethod
    def _safe_int(value: Any, default: int = 0) -> int:
        """Safely convert value to integer"""
        if pd.isna(value) or value is None:
            return default
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return default
    
    @staticmethod
    def _safe_bool(value: Any) -> bool:
        """Safely convert value to boolean"""
        if pd.isna(value) or value is None:
            return True
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ['true', 'yes', '1', 't', 'y']
        return bool(value)

class DataLoader:
    """Main data loader class that handles multiple data sources"""
    
    def __init__(self, db: Session):
        self.db = db
        self.whatsapp_parser = WhatsAppParser()
        self.csv_loader = CSVLoader()
    
    def load_whatsapp_messages(self, messages: List[str]) -> Dict[str, Any]:
        """Load and process WhatsApp messages"""
        results = {
            'train_updates': [],
            'maintenance_updates': [],
            'fitness_updates': [],
            'cleaning_updates': [],
            'errors': []
        }
        
        for message in messages:
            parsed_data = self.whatsapp_parser.parse_message(message)
            
            if parsed_data['type'] == 'error':
                results['errors'].append(parsed_data)
            elif parsed_data['type'] == 'train_status':
                results['train_updates'].append(parsed_data)
            elif parsed_data['type'] == 'maintenance_update':
                results['maintenance_updates'].append(parsed_data)
            elif parsed_data['type'] == 'fitness_update':
                results['fitness_updates'].append(parsed_data)
            elif parsed_data['type'] == 'cleaning_schedule':
                results['cleaning_updates'].append(parsed_data)
        
        return results
    
    def load_csv_file(self, file_path: str, data_type: str) -> Dict[str, Any]:
        """Load data from CSV file based on type"""
        try:
            if data_type == 'trains':
                data = self.csv_loader.load_trains_csv(file_path)
            elif data_type == 'fitness':
                data = self.csv_loader.load_fitness_csv(file_path)
            elif data_type == 'job_cards':
                data = self.csv_loader.load_job_cards_csv(file_path)
            elif data_type == 'branding':
                data = self.csv_loader.load_branding_csv(file_path)
            else:
                return {'success': False, 'error': f'Unknown data type: {data_type}'}
            
            return {
                'success': True,
                'data_type': data_type,
                'records_loaded': len(data),
                'data': data
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def save_to_database(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Save loaded data to database"""
        results = {
            'trains_created': 0,
            'fitness_certs_created': 0,
            'job_cards_created': 0,
            'branding_contracts_created': 0,
            'errors': []
        }
        
        # Process trains data - FIXED: Convert dict to schema object
        if 'trains' in data:
            for train_data in data['trains']:
                try:
                    train_number = train_data.get('train_number')
                    if not train_number:
                        results['errors'].append("Train record missing train number")
                        continue
                    
                    # Check if train exists
                    existing_train = crud.trains.read_train_by_number(self.db, train_number)
                    
                    if existing_train:
                        # Update existing train
                        update_data = {}
                        for key, value in train_data.items():
                            if hasattr(existing_train, key) and value is not None:
                                update_data[key] = value
                        
                        if update_data:
                            crud.trains.update_train(self.db, existing_train.id, update_data)
                    else:
                        # Create new train - Convert dict to schema object
                        train_schema = self._create_train_schema(train_data)
                        if train_schema:
                            crud.trains.create_train(self.db, train_schema)
                            results['trains_created'] += 1
                        else:
                            results['errors'].append(f"Train {train_number}: Invalid data schema")
                            
                except Exception as e:
                    results['errors'].append(f"Train {train_data.get('train_number', 'Unknown')}: {str(e)}")
        
        # Process fitness certificates - FIXED: Convert dict to schema object
        if 'fitness_certificates' in data:
            for cert_data in data['fitness_certificates']:
                try:
                    train_number = cert_data.get('train_number')
                    if not train_number:
                        results['errors'].append("Fitness certificate missing train number")
                        continue
                    
                    train = crud.trains.read_train_by_number(self.db, train_number)
                    if train:
                        cert_data['train_id'] = train.id
                        # Convert dict to schema object
                        cert_schema = self._create_fitness_schema(cert_data)
                        if cert_schema:
                            crud.fitness_certificates.create_fitness_certificate(self.db, cert_schema)
                            results['fitness_certs_created'] += 1
                        else:
                            results['errors'].append(f"Fitness cert for {train_number}: Invalid data schema")
                    else:
                        results['errors'].append(f"Train {train_number} not found for fitness certificate")
                except Exception as e:
                    results['errors'].append(f"Fitness cert for {cert_data.get('train_number', 'Unknown')}: {str(e)}")
        
        # Process job cards - FIXED: Convert dict to schema object
        if 'job_cards' in data:
            for job_data in data['job_cards']:
                try:
                    train_number = job_data.get('train_number')
                    if not train_number:
                        results['errors'].append("Job card missing train number")
                        continue
                    
                    train = crud.trains.read_train_by_number(self.db, train_number)
                    if train:
                        job_data['train_id'] = train.id
                        # Convert dict to schema object
                        job_schema = self._create_job_card_schema(job_data)
                        if job_schema:
                            crud.job_cards.create_job_card(self.db, job_schema)
                            results['job_cards_created'] += 1
                        else:
                            results['errors'].append(f"Job card for {train_number}: Invalid data schema")
                    else:
                        results['errors'].append(f"Train {train_number} not found for job card")
                except Exception as e:
                    results['errors'].append(f"Job card for {job_data.get('train_number', 'Unknown')}: {str(e)}")
        
        # Process branding contracts - FIXED: Convert dict to schema object
        if 'branding_contracts' in data:
            for contract_data in data['branding_contracts']:
                try:
                    train_number = contract_data.get('train_number')
                    if not train_number:
                        results['errors'].append("Branding contract missing train number")
                        continue
                    
                    train = crud.trains.read_train_by_number(self.db, train_number)
                    if train:
                        contract_data['train_id'] = train.id
                        # Convert dict to schema object
                        contract_schema = self._create_branding_schema(contract_data)
                        if contract_schema:
                            crud.branding_contracts.create_branding_contract(self.db, contract_schema)
                            results['branding_contracts_created'] += 1
                        else:
                            results['errors'].append(f"Branding contract for {train_number}: Invalid data schema")
                    else:
                        results['errors'].append(f"Train {train_number} not found for branding contract")
                except Exception as e:
                    results['errors'].append(f"Branding contract for {contract_data.get('train_number', 'Unknown')}: {str(e)}")
        
        return results
    
    def _create_train_schema(self, data: Dict[str, Any]) -> Optional[schemas.TrainCreate]:
        """Convert train dictionary to schema object"""
        try:
            return schemas.TrainCreate(
                train_number=data.get('train_number'),
                train_name=data.get('train_name'),
                capacity=data.get('capacity'),
                model=data.get('model'),
                status=data.get('status', 'active'),
                current_mileage=data.get('current_mileage', 0),
                last_maintenance_date=data.get('last_maintenance_date'),
                coaches=data.get('coaches'),
                max_speed=data.get('max_speed')
            )
        except Exception as e:
            print(f"Error creating train schema: {e}")
            return None
    
    def _create_fitness_schema(self, data: Dict[str, Any]) -> Optional[schemas.FitnessCertificateCreate]:
        """Convert fitness certificate dictionary to schema object"""
        try:
            return schemas.FitnessCertificateCreate(
                train_id=data.get('train_id'),
                department=data.get('department'),
                valid_from=data.get('valid_from'),
                valid_until=data.get('valid_until'),
                is_valid=data.get('is_valid', True)
            )
        except Exception as e:
            print(f"Error creating fitness schema: {e}")
            return None
    
    def _create_job_card_schema(self, data: Dict[str, Any]) -> Optional[schemas.JobCardCreate]:
        """Convert job card dictionary to schema object"""
        try:
            return schemas.JobCardCreate(
                train_id=data.get('train_id'),
                work_order_id=data.get('work_order_id'),
                status=data.get('status', 'open'),
                description=data.get('description', ''),
                scheduled_date=data.get('scheduled_date'),
                completed_date=data.get('completed_date'),
                estimated_hours=data.get('estimated_hours')
            )
        except Exception as e:
            print(f"Error creating job card schema: {e}")
            return None
    
    def _create_branding_schema(self, data: Dict[str, Any]) -> Optional[schemas.BrandingContractCreate]:
        """Convert branding contract dictionary to schema object"""
        try:
            return schemas.BrandingContractCreate(
                train_id=data.get('train_id'),
                advertiser_name=data.get('advertiser_name'),
                exposure_hours_required=data.get('exposure_hours_required', 0),
                exposure_hours_fulfilled=data.get('exposure_hours_fulfilled', 0),
                start_date=data.get('start_date'),
                end_date=data.get('end_date')
            )
        except Exception as e:
            print(f"Error creating branding schema: {e}")
            return None
    
    def process_whatsapp_updates(self, messages: List[str]) -> Dict[str, Any]:
        """Process WhatsApp messages and update database"""
        parsed_data = self.load_whatsapp_messages(messages)
        results = {
            'messages_processed': len(messages),
            'updates_applied': 0,
            'errors': parsed_data['errors']
        }
        
        # Process train status updates
        for update in parsed_data['train_updates']:
            try:
                train = crud.trains.read_train_by_number(self.db, update.get('train_number'))
                if train:
                    update_data = {}
                    if 'status' in update:
                        update_data['status'] = update['status']
                    if 'mileage' in update:
                        update_data['current_mileage'] = int(update['mileage'])
                    
                    if update_data:
                        crud.trains.update_train(self.db, train.id, update_data)
                        results['updates_applied'] += 1
            except Exception as e:
                results['errors'].append(f"Train update error: {str(e)}")
        
        return results