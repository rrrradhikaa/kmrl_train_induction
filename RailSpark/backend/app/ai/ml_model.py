import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline
import joblib
from sqlalchemy.orm import Session
from datetime import date, timedelta, datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import logging
import warnings
import os
import sys
from pathlib import Path
import requests
import json
from io import StringIO
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/ml_model.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Suppress warnings
warnings.filterwarnings('ignore')

@dataclass
class FailurePrediction:
    train_id: int
    train_number: str
    failure_probability: float
    risk_level: str
    predicted_failure_type: Optional[str]
    confidence: float
    recommendation: str
    features: Dict[str, Any]
    model_used: str
    prediction_timestamp: datetime

class MLModel:
    def __init__(self, db: Session, auto_retrain_days: int = 30):
        self.db = db
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.scaler = None
        self.imputer = None
        self.feature_names = []
        self.model_dir = Path("models")
        self.auto_retrain_days = auto_retrain_days
        self.last_training_date = None
        self.is_trained = False
        self.historical_data_sources = [
            "https://raw.githubusercontent.com/datasets/railway-accidents/master/data/accidents.csv",
            "https://raw.githubusercontent.com/datasets/vehicle-maintenance/master/data/maintenance.csv"
        ]
        
        # Create directories
        self.model_dir.mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        Path("data").mkdir(exist_ok=True)
        
        # Model configurations
        self.model_configs = {
            'random_forest': {
                'model': RandomForestClassifier(n_estimators=100, random_state=42),
                'params': {
                    'n_estimators': [50, 100],
                    'max_depth': [5, 10, None],
                    'min_samples_split': [2, 5]
                }
            },
            'gradient_boosting': {
                'model': GradientBoostingClassifier(n_estimators=100, random_state=42),
                'params': {
                    'n_estimators': [50, 100],
                    'learning_rate': [0.05, 0.1],
                    'max_depth': [3, 5]
                }
            }
        }
        
        # Define the expected feature order
        self.base_features = [
            'mileage', 'train_age_days', 'maintenance_age_days', 'open_jobs_count',
            'cert_validity_days', 'has_active_branding', 'cleaning_slots_count', 
            'induction_priority'
        ]
        
        self.derived_features = [
            'mileage_per_year', 'maintenance_ratio', 'utilization_intensity', 'maintenance_urgency'
        ]
        
        self.expected_features = self.base_features + self.derived_features
        
        # Initialize model
        self.initialize_model()
    
    def initialize_model(self):
        """Initialize model - load existing or train new with historical data"""
        try:
            if self.load_model():
                logger.info("Model loaded successfully from disk")
                self.is_trained = True
                self.check_retraining_need()
            else:
                logger.info("No existing model found. Training new model with historical data...")
                result = self.train_model_with_historical_data()
                if result["success"]:
                    self.is_trained = True
                    logger.info("Model trained successfully with historical data")
                else:
                    logger.warning("Historical data training failed. Trying synthetic data...")
                    self.train_with_synthetic_data()
        except Exception as e:
            logger.error(f"Error initializing model: {e}")
            # Train with synthetic data as fallback
            self.train_with_synthetic_data()
    
    def _ensure_feature_consistency(self, features: Dict[str, Any]) -> np.ndarray:
        """Ensure features match the expected format and order"""
        try:
            # Create a template with all expected features set to 0
            template = {feature: 0.0 for feature in self.expected_features}
            
            # Update with actual features
            template.update(features)
            
            # Ensure all derived features are calculated
            if any(feature not in features for feature in self.derived_features):
                template.update(self._calculate_derived_features(template))
            
            # Return features in consistent order
            feature_array = np.array([template[feature] for feature in self.expected_features])
            return feature_array.reshape(1, -1)
            
        except Exception as e:
            logger.error(f"Error ensuring feature consistency: {e}")
            # Return zero array as fallback
            return np.zeros((1, len(self.expected_features)))
    
    def _extract_features_from_train(self, train) -> Dict[str, Any]:
        """Extract features from train object using your schema"""
        try:
            features = {
                'mileage': float(getattr(train, 'current_mileage', 0)),
                'train_age_days': float(self._calculate_train_age(train)),
                'maintenance_age_days': float(self._calculate_maintenance_age(train)),
                'open_jobs_count': float(self._get_open_jobs_count(train.id)),
                'cert_validity_days': float(self._get_certificate_validity(train.id)),
                'has_active_branding': float(self._has_active_branding(train.id)),
                'cleaning_slots_count': float(self._get_cleaning_slots_count(train.id)),
                'induction_priority': float(self._get_induction_priority(train.id)),
            }
            
            # Add derived features
            features.update(self._calculate_derived_features(features))
            
            return features
        except Exception as e:
            logger.error(f"Error extracting features from train {train.id}: {e}")
            # Return default features
            return self._get_default_features()
    
    def _get_default_features(self) -> Dict[str, Any]:
        """Get default feature values when extraction fails"""
        return {feature: 0.0 for feature in self.expected_features}
    
    def _prepare_features_for_prediction(self, features: Dict[str, Any]) -> np.ndarray:
        """Prepare features for prediction with proper imputation and scaling"""
        try:
            # Ensure feature consistency
            feature_array = self._ensure_feature_consistency(features)
            
            # Apply imputation if available
            if self.imputer:
                feature_array = self.imputer.transform(feature_array)
            
            # Apply scaling if available
            if self.scaler:
                feature_array = self.scaler.transform(feature_array)
            
            return feature_array
            
        except Exception as e:
            logger.error(f"Error preparing features for prediction: {e}")
            # Return zero array as fallback
            return np.zeros((1, len(self.expected_features)))
    
    def download_historical_data(self) -> pd.DataFrame:
        """Download and combine historical train failure data from multiple sources"""
        logger.info("Downloading historical train data...")
        
        all_data = []
        
        for source in self.historical_data_sources:
            try:
                logger.info(f"Downloading from {source}")
                response = requests.get(source, timeout=30)
                response.raise_for_status()
                
                # Parse the data based on source type
                if "accidents" in source:
                    df = self._parse_accident_data(response.text)
                elif "maintenance" in source:
                    df = self._parse_maintenance_data(response.text)
                else:
                    df = self._parse_generic_data(response.text)
                
                if not df.empty:
                    all_data.append(df)
                    logger.info(f"Downloaded {len(df)} records from {source}")
                
            except Exception as e:
                logger.warning(f"Failed to download from {source}: {e}")
                continue
        
        # Also try to load local historical data if available
        local_data = self._load_local_historical_data()
        if local_data is not None:
            all_data.append(local_data)
        
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
            logger.info(f"Combined {len(combined_data)} historical records")
            return combined_data
        else:
            logger.warning("No historical data could be downloaded")
            return pd.DataFrame()
    
    def _parse_accident_data(self, csv_text: str) -> pd.DataFrame:
        """Parse accident/incident data"""
        try:
            df = pd.read_csv(StringIO(csv_text))
            
            # Map columns to our feature format
            feature_mapping = {
                'mileage': 'mileage',
                'age': 'train_age_days',
                'days_since_maintenance': 'maintenance_age_days',
                'open_issues': 'open_jobs_count',
                'utilization': 'mileage_per_year',
            }
            
            # Create features dictionary
            features_list = []
            for _, row in df.iterrows():
                features = {
                    'mileage': float(row.get('mileage', np.random.randint(10000, 150000))),
                    'train_age_days': float(row.get('age', np.random.randint(365, 3650))),
                    'maintenance_age_days': float(row.get('days_since_maintenance', np.random.randint(30, 730))),
                    'open_jobs_count': float(row.get('open_issues', np.random.poisson(1.5))),
                    'cert_validity_days': float(np.random.randint(0, 365)),
                    'has_active_branding': float(np.random.choice([0, 1], p=[0.7, 0.3])),
                    'cleaning_slots_count': float(np.random.poisson(0.5)),
                    'induction_priority': float(np.random.choice([1, 2, 3, 99], p=[0.2, 0.3, 0.3, 0.2])),
                }
                
                # Add derived features
                features.update(self._calculate_derived_features(features))
                
                # Use actual failure data if available, otherwise simulate
                if 'failure_occurred' in row:
                    features['failure_occurred'] = int(row['failure_occurred'])
                else:
                    features['failure_occurred'] = self._simulate_failure_risk(features)
                
                features_list.append(features)
            
            result_df = pd.DataFrame(features_list)
            # Ensure all expected features are present
            for feature in self.expected_features + ['failure_occurred']:
                if feature not in result_df.columns:
                    result_df[feature] = 0.0
            return result_df
            
        except Exception as e:
            logger.error(f"Error parsing accident data: {e}")
            return pd.DataFrame()
    
    def _parse_maintenance_data(self, csv_text: str) -> pd.DataFrame:
        """Parse maintenance record data"""
        try:
            df = pd.read_csv(StringIO(csv_text))
            
            features_list = []
            for _, row in df.iterrows():
                features = {
                    'mileage': float(row.get('current_mileage', np.random.randint(10000, 150000))),
                    'train_age_days': float(row.get('train_age_days', np.random.randint(365, 3650))),
                    'maintenance_age_days': float(row.get('days_since_last_maintenance', np.random.randint(30, 730))),
                    'open_jobs_count': float(row.get('pending_jobs', np.random.poisson(1.5))),
                    'cert_validity_days': float(np.random.randint(0, 365)),
                    'has_active_branding': float(np.random.choice([0, 1], p=[0.7, 0.3])),
                    'cleaning_slots_count': float(np.random.poisson(0.5)),
                    'induction_priority': float(np.random.choice([1, 2, 3, 99], p=[0.2, 0.3, 0.3, 0.2])),
                }
                
                # Add derived features
                features.update(self._calculate_derived_features(features))
                
                # Determine failure based on maintenance patterns
                if 'maintenance_urgency' in row:
                    features['failure_occurred'] = 1 if row['maintenance_urgency'] > 0.7 else 0
                else:
                    features['failure_occurred'] = self._simulate_failure_risk(features)
                
                features_list.append(features)
            
            result_df = pd.DataFrame(features_list)
            # Ensure all expected features are present
            for feature in self.expected_features + ['failure_occurred']:
                if feature not in result_df.columns:
                    result_df[feature] = 0.0
            return result_df
            
        except Exception as e:
            logger.error(f"Error parsing maintenance data: {e}")
            return pd.DataFrame()
    
    def _parse_generic_data(self, csv_text: str) -> pd.DataFrame:
        """Parse generic railway data"""
        try:
            df = pd.read_csv(StringIO(csv_text))
            
            # Extract relevant columns or create synthetic data
            features_list = []
            for _, row in df.iterrows():
                features = {
                    'mileage': float(row.get('mileage', np.random.randint(10000, 150000))),
                    'train_age_days': float(row.get('age_days', np.random.randint(365, 3650))),
                    'maintenance_age_days': float(row.get('maintenance_interval', np.random.randint(30, 730))),
                    'open_jobs_count': float(np.random.poisson(1.5)),
                    'cert_validity_days': float(np.random.randint(0, 365)),
                    'has_active_branding': float(np.random.choice([0, 1], p=[0.7, 0.3])),
                    'cleaning_slots_count': float(np.random.poisson(0.5)),
                    'induction_priority': float(np.random.choice([1, 2, 3, 99], p=[0.2, 0.3, 0.3, 0.2])),
                }
                
                features.update(self._calculate_derived_features(features))
                features['failure_occurred'] = self._simulate_failure_risk(features)
                features_list.append(features)
            
            result_df = pd.DataFrame(features_list)
            # Ensure all expected features are present
            for feature in self.expected_features + ['failure_occurred']:
                if feature not in result_df.columns:
                    result_df[feature] = 0.0
            return result_df
            
        except Exception as e:
            logger.error(f"Error parsing generic data: {e}")
            return pd.DataFrame()
    
    def _load_local_historical_data(self) -> Optional[pd.DataFrame]:
        """Load historical data from local files if available"""
        local_paths = [
            "data/historical_train_data.csv",
            "data/train_maintenance_records.csv",
            "data/railway_failure_data.csv"
        ]
        
        for path in local_paths:
            if os.path.exists(path):
                try:
                    df = pd.read_csv(path)
                    logger.info(f"Loaded local historical data from {path}")
                    
                    # Process local data
                    features_list = []
                    for _, row in df.iterrows():
                        features = {
                            'mileage': float(row.get('mileage', np.random.randint(10000, 150000))),
                            'train_age_days': float(row.get('train_age_days', np.random.randint(365, 3650))),
                            'maintenance_age_days': float(row.get('maintenance_age_days', np.random.randint(30, 730))),
                            'open_jobs_count': float(row.get('open_jobs_count', np.random.poisson(1.5))),
                            'cert_validity_days': float(row.get('cert_validity_days', np.random.randint(0, 365))),
                            'has_active_branding': float(row.get('has_active_branding', np.random.choice([0, 1]))),
                            'cleaning_slots_count': float(row.get('cleaning_slots_count', np.random.poisson(0.5))),
                            'induction_priority': float(row.get('induction_priority', np.random.choice([1, 2, 3, 99]))),
                        }
                        
                        features.update(self._calculate_derived_features(features))
                        
                        if 'failure_occurred' in row:
                            features['failure_occurred'] = int(row['failure_occurred'])
                        else:
                            features['failure_occurred'] = self._simulate_failure_risk(features)
                        
                        features_list.append(features)
                    
                    result_df = pd.DataFrame(features_list)
                    # Ensure all expected features are present
                    for feature in self.expected_features + ['failure_occurred']:
                        if feature not in result_df.columns:
                            result_df[feature] = 0.0
                    return result_df
                    
                except Exception as e:
                    logger.error(f"Error loading local data from {path}: {e}")
        
        return None
    
    def train_model_with_historical_data(self) -> Dict[str, Any]:
        """Train model using downloaded historical data"""
        logger.info("Training model with historical data...")
        
        try:
            # Download historical data
            historical_df = self.download_historical_data()
            
            if historical_df.empty:
                logger.warning("No historical data available. Using synthetic data.")
                return self.train_with_synthetic_data()
            
            # Combine with current data if available
            current_df = self.prepare_training_data()
            
            if not current_df.empty:
                combined_df = pd.concat([historical_df, current_df], ignore_index=True)
                logger.info(f"Combined historical data ({len(historical_df)} records) with current data ({len(current_df)} records)")
            else:
                combined_df = historical_df
                logger.info(f"Using historical data only: {len(historical_df)} records")
            
            # Train on combined dataset
            return self._train_on_dataframe(combined_df)
            
        except Exception as e:
            logger.error(f"Error training with historical data: {e}")
            return {"success": False, "error": str(e)}
    
    def train_with_synthetic_data(self, n_samples: int = 2000) -> Dict[str, Any]:
        """Train model using comprehensive synthetic data"""
        logger.info(f"Training with {n_samples} synthetic samples...")
        
        try:
            df = self._generate_comprehensive_synthetic_data(n_samples)
            result = self._train_on_dataframe(df)
            
            if result["success"]:
                self.is_trained = True
                logger.info("Model trained successfully with synthetic data")
            
            return result
            
        except Exception as e:
            logger.error(f"Error training with synthetic data: {e}")
            return {"success": False, "error": str(e)}
    
    def _generate_comprehensive_synthetic_data(self, n_samples: int = 2000) -> pd.DataFrame:
        """Generate realistic synthetic training data with varied patterns"""
        logger.info(f"Generating {n_samples} comprehensive synthetic samples")
        
        np.random.seed(42)
        data = []
        
        # Create different patterns for failure scenarios
        patterns = {
            'high_mileage_failure': {'mileage_range': (80000, 150000), 'failure_prob': 0.7},
            'poor_maintenance': {'maintenance_range': (180, 730), 'failure_prob': 0.8},
            'high_utilization': {'utilization_range': (25000, 50000), 'failure_prob': 0.6},
            'multiple_issues': {'open_jobs_range': (3, 10), 'failure_prob': 0.9},
            'normal_operation': {'failure_prob': 0.1}
        }
        
        samples_per_pattern = n_samples // len(patterns)
        
        for pattern_name, pattern_config in patterns.items():
            for i in range(samples_per_pattern):
                if pattern_name == 'high_mileage_failure':
                    mileage = np.random.randint(*pattern_config['mileage_range'])
                    maintenance_age = np.random.randint(30, 365)
                    open_jobs = np.random.poisson(2)
                elif pattern_name == 'poor_maintenance':
                    mileage = np.random.randint(10000, 80000)
                    maintenance_age = np.random.randint(*pattern_config['maintenance_range'])
                    open_jobs = np.random.poisson(3)
                elif pattern_name == 'high_utilization':
                    mileage = np.random.randint(50000, 120000)
                    train_age = np.random.randint(365, 1095)  # 1-3 years
                    maintenance_age = np.random.randint(60, 180)
                    open_jobs = np.random.poisson(1)
                elif pattern_name == 'multiple_issues':
                    mileage = np.random.randint(20000, 100000)
                    maintenance_age = np.random.randint(120, 365)
                    open_jobs = np.random.randint(*pattern_config['open_jobs_range'])
                else:  # normal_operation
                    mileage = np.random.randint(5000, 60000)
                    maintenance_age = np.random.randint(1, 90)
                    open_jobs = np.random.poisson(0.5)
                
                features = {
                    'mileage': float(mileage),
                    'train_age_days': float(np.random.randint(365, 3650)),
                    'maintenance_age_days': float(maintenance_age),
                    'open_jobs_count': float(open_jobs),
                    'cert_validity_days': float(np.random.randint(0, 365)),
                    'has_active_branding': float(np.random.choice([0, 1], p=[0.7, 0.3])),
                    'cleaning_slots_count': float(np.random.poisson(0.5)),
                    'induction_priority': float(np.random.choice([1, 2, 3, 99], p=[0.2, 0.3, 0.3, 0.2])),
                }
                
                # Add derived features
                features.update(self._calculate_derived_features(features))
                
                # Determine failure based on pattern
                if np.random.random() < pattern_config['failure_prob']:
                    features['failure_occurred'] = 1
                else:
                    features['failure_occurred'] = 0
                
                features['train_id'] = len(data)
                data.append(features)
        
        # Add some random samples
        for i in range(n_samples - len(data)):
            features = {
                'mileage': float(np.random.randint(1000, 150000)),
                'train_age_days': float(np.random.randint(365, 3650)),
                'maintenance_age_days': float(np.random.randint(1, 730)),
                'open_jobs_count': float(np.random.poisson(1.5)),
                'cert_validity_days': float(np.random.randint(0, 365)),
                'has_active_branding': float(np.random.choice([0, 1], p=[0.7, 0.3])),
                'cleaning_slots_count': float(np.random.poisson(0.5)),
                'induction_priority': float(np.random.choice([1, 2, 3, 99], p=[0.2, 0.3, 0.3, 0.2])),
            }
            
            features.update(self._calculate_derived_features(features))
            features['failure_occurred'] = self._simulate_failure_risk(features)
            features['train_id'] = len(data)
            data.append(features)
        
        df = pd.DataFrame(data)
        logger.info(f"Generated synthetic dataset with {len(df)} samples")
        logger.info(f"Failure distribution: {df['failure_occurred'].value_counts().to_dict()}")
        
        return df

    # === ALL ORIGINAL METHODS ===
    
    def _get_train_model(self):
        """Dynamically import Train model to avoid circular imports"""
        from models import Train
        return Train
    
    def _calculate_train_age(self, train) -> int:
        """Calculate train age in days"""
        try:
            if hasattr(train, 'commissioning_date') and train.commissioning_date:
                return (date.today() - train.commissioning_date).days
        except:
            pass
        return 365 * 3  # Default 3 years
    
    def _calculate_maintenance_age(self, train) -> int:
        """Calculate days since last maintenance"""
        try:
            if hasattr(train, 'last_maintenance_date') and train.last_maintenance_date:
                return (date.today() - train.last_maintenance_date).days
        except:
            pass
        return 365  # Default 1 year
    
    def _get_open_jobs_count(self, train_id: int) -> int:
        """Get count of open job cards for train"""
        try:
            from models import JobCard
            open_jobs = self.db.query(JobCard).filter(
                JobCard.train_id == train_id,
                JobCard.status == "open"
            ).all()
            return len(open_jobs)
        except:
            return 0
    
    def _get_certificate_validity(self, train_id: int) -> int:
        """Get minimum certificate validity days"""
        try:
            from models import FitnessCertificate
            today = date.today()
            valid_certs = self.db.query(FitnessCertificate).filter(
                FitnessCertificate.train_id == train_id,
                FitnessCertificate.valid_from <= today,
                FitnessCertificate.valid_until >= today,
                FitnessCertificate.is_valid == True
            ).all()
            
            if valid_certs:
                return min((cert.valid_until - today).days for cert in valid_certs)
            return 0
        except:
            return 0
    
    def _has_active_branding(self, train_id: int) -> int:
        """Check if train has active branding contracts"""
        try:
            from models import BrandingContract
            today = date.today()
            active_contracts = self.db.query(BrandingContract).filter(
                BrandingContract.train_id == train_id,
                BrandingContract.start_date <= today,
                BrandingContract.end_date >= today
            ).all()
            return len(active_contracts) > 0
        except:
            return 0
    
    def _get_cleaning_slots_count(self, train_id: int) -> int:
        """Get count of upcoming cleaning slots"""
        try:
            from models import CleaningSlot
            from datetime import datetime
            upcoming_slots = self.db.query(CleaningSlot).filter(
                CleaningSlot.train_id == train_id,
                CleaningSlot.slot_time >= datetime.now(),
                CleaningSlot.status == "scheduled"
            ).all()
            return len(upcoming_slots)
        except:
            return 0
    
    def _get_induction_priority(self, train_id: int) -> int:
        """Get induction priority from today's plan"""
        try:
            from models import InductionPlan
            today = date.today()
            today_plan = self.db.query(InductionPlan).filter(
                InductionPlan.train_id == train_id,
                InductionPlan.plan_date == today
            ).first()
            
            if today_plan and today_plan.rank:
                return today_plan.rank
            return 99  # Low priority if not scheduled
        except:
            return 99
    
    def _calculate_derived_features(self, features: Dict) -> Dict[str, Any]:
        """Calculate derived features from basic features"""
        try:
            mileage = features.get('mileage', 0)
            train_age = max(features.get('train_age_days', 1095), 1)  # Avoid division by zero
            maintenance_age = features.get('maintenance_age_days', 365)
            
            return {
                'mileage_per_year': float(mileage / (train_age / 365)),
                'maintenance_ratio': float(maintenance_age / 180),  # Ratio to 6-month standard
                'utilization_intensity': float(min(mileage / (train_age / 365) / 20000, 3.0)),  # Normalized
                'maintenance_urgency': float(min(maintenance_age / 90, 4.0)),  # Urgency score
            }
        except Exception as e:
            logger.error(f"Error calculating derived features: {e}")
            return {
                'mileage_per_year': 0.0,
                'maintenance_ratio': 0.0,
                'utilization_intensity': 0.0,
                'maintenance_urgency': 0.0,
            }
    
    def _simulate_failure_risk(self, features: Dict) -> int:
        """Simulate failure risk based on features (for training data)"""
        risk_score = 0
        
        # High mileage risk
        if features.get('mileage', 0) > 50000:
            risk_score += 2
        elif features.get('mileage', 0) > 20000:
            risk_score += 1
        
        # Maintenance age risk
        if features.get('maintenance_age_days', 0) > 180:
            risk_score += 2
        elif features.get('maintenance_age_days', 0) > 90:
            risk_score += 1
        
        # Open jobs risk
        if features.get('open_jobs_count', 0) > 5:
            risk_score += 2
        elif features.get('open_jobs_count', 0) > 2:
            risk_score += 1
        
        # Certificate risk
        if features.get('cert_validity_days', 0) < 30:
            risk_score += 1
        
        # High utilization risk
        if features.get('mileage_per_year', 0) > 25000:
            risk_score += 1
        
        return 1 if risk_score >= 3 else 0
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values safely"""
        df_clean = df.copy()
        numeric_features = df_clean.select_dtypes(include=[np.number]).columns.tolist()
        
        if 'failure_occurred' in numeric_features:
            numeric_features.remove('failure_occurred')
        
        if numeric_features:
            self.imputer = SimpleImputer(strategy='median')
            df_clean[numeric_features] = self.imputer.fit_transform(df_clean[numeric_features])
        
        return df_clean
    
    def _handle_class_imbalance(self, X: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Handle class imbalance using SMOTE with better error handling"""
        try:
            unique, counts = np.unique(y, return_counts=True)
            if len(unique) < 2 or min(counts) < 2:
                logger.warning("Not enough samples for class balancing")
                return X, y
            
            # Use different strategies based on class distribution
            ratio = min(counts[1] / counts[0], 0.8) if counts[0] > counts[1] else min(counts[0] / counts[1], 0.8)
            
            smote = SMOTE(random_state=42, sampling_strategy=ratio)
            X_balanced, y_balanced = smote.fit_resample(X, y)
            
            logger.info(f"Class balancing applied: {dict(zip(unique, counts))} -> {dict(zip(*np.unique(y_balanced, return_counts=True)))}")
            return X_balanced, y_balanced
        except Exception as e:
            logger.warning(f"Class balancing failed, using original data: {e}")
            return X, y
    
    def prepare_training_data(self) -> pd.DataFrame:
        """Prepare training data using available CRUD functions"""
        logger.info("Preparing training data...")
        
        try:
            # Get trains using your CRUD function
            trains = self.db.query(self._get_train_model()).all()
            data = []
            
            for train in trains:
                features = self._extract_features_from_train(train)
                # Simulate target variable based on features
                features['failure_occurred'] = self._simulate_failure_risk(features)
                features['train_id'] = train.id
                data.append(features)
            
            if not data:
                logger.warning("No train data found. Will use historical data only.")
                return pd.DataFrame()
            
            df = pd.DataFrame(data)
            logger.info(f"Prepared dataset with {len(df)} samples")
            return df
            
        except Exception as e:
            logger.error(f"Error preparing training data: {e}")
            return pd.DataFrame()
    
    def _train_on_dataframe(self, df: pd.DataFrame, test_size: float = 0.2) -> Dict[str, Any]:
        """Train model on a prepared DataFrame with consistent feature handling"""
        if len(df) < 10:
            return {"success": False, "message": "Insufficient data for training"}
        
        try:
            # Ensure all expected features are present
            for feature in self.expected_features:
                if feature not in df.columns:
                    df[feature] = 0.0  # Add missing features with default value
            
            # Handle missing values
            df_clean = self._handle_missing_values(df)
            
            # Use only the expected features in consistent order
            X = df_clean[self.expected_features]
            y = df_clean['failure_occurred']
            
            # Scale features
            self.scaler = RobustScaler()
            X_scaled = self.scaler.fit_transform(X)
            
            # Handle class imbalance with better strategy
            X_balanced, y_balanced = self._handle_class_imbalance(X_scaled, y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X_balanced, y_balanced, test_size=test_size, random_state=42, stratify=y_balanced
            )
            
            # Train models with cross-validation
            performance_results = {}
            
            for model_name, config in self.model_configs.items():
                try:
                    logger.info(f"Training {model_name}...")
                    
                    # Use GridSearchCV for hyperparameter tuning
                    grid_search = GridSearchCV(
                        config['model'],
                        config['params'],
                        cv=StratifiedKFold(n_splits=min(5, len(X_train)//5), shuffle=True, random_state=42),
                        scoring='f1',
                        n_jobs=-1,
                        verbose=0
                    )
                    
                    grid_search.fit(X_train, y_train)
                    best_model = grid_search.best_estimator_
                    self.models[model_name] = best_model
                    
                    # Evaluate
                    y_pred = best_model.predict(X_test)
                    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
                    
                    # Cross-validation scores
                    cv_scores = cross_val_score(best_model, X_train, y_train, 
                                              cv=StratifiedKFold(n_splits=min(5, len(X_train)//5)), 
                                              scoring='f1')
                    
                    performance = {
                        'accuracy': accuracy_score(y_test, y_pred),
                        'precision': precision_score(y_test, y_pred, zero_division=0),
                        'recall': recall_score(y_test, y_pred, zero_division=0),
                        'f1_score': f1_score(y_test, y_pred, zero_division=0),
                        'roc_auc': roc_auc_score(y_test, y_pred_proba),
                        'cross_val_mean': cv_scores.mean(),
                        'cross_val_std': cv_scores.std(),
                        'best_params': grid_search.best_params_,
                        'feature_importance': dict(zip(self.expected_features, best_model.feature_importances_))
                    }
                    
                    performance_results[model_name] = performance
                    logger.info(f"{model_name} trained - F1: {performance['f1_score']:.3f}, AUC: {performance['roc_auc']:.3f}")
                    
                except Exception as e:
                    logger.error(f"Error training {model_name}: {e}")
                    continue
            
            if not performance_results:
                return {"success": False, "message": "No models trained successfully"}
            
            # Select best model based on F1 score
            self.best_model_name = max(performance_results.keys(), 
                                     key=lambda x: performance_results[x]['f1_score'])
            self.best_model = self.models[self.best_model_name]
            
            # Set feature names for consistency
            self.feature_names = self.expected_features
            
            self.last_training_date = datetime.now()
            self.is_trained = True
            self.save_model()
            
            return {
                "success": True,
                "best_model": self.best_model_name,
                "performance": performance_results,
                "training_samples": len(X_train),
                "test_samples": len(X_test),
                "feature_importance": performance_results[self.best_model_name]['feature_importance'],
                "cross_validation_score": performance_results[self.best_model_name]['cross_val_mean']
            }
            
        except Exception as e:
            logger.error(f"Error in _train_on_dataframe: {e}")
            return {"success": False, "error": str(e)}
    
    def train_model(self, test_size: float = 0.2) -> Dict[str, Any]:
        """Train the failure prediction model (main entry point)"""
        try:
            # First try with historical data
            result = self.train_model_with_historical_data()
            if result["success"]:
                return result
            else:
                # Fallback to synthetic data
                return self.train_with_synthetic_data()
        except Exception as e:
            logger.error(f"Error in train_model: {e}")
            return self.train_with_synthetic_data()  # Final fallback
    
    def predict_failure_risk(self, train_id: int) -> FailurePrediction:
        """Predict failure risk for a specific train"""
        if not self.is_trained or not self.best_model:
            raise ValueError("Model not trained. Call train_model() first.")
        
        try:
            # Get train from database
            Train = self._get_train_model()
            train = self.db.query(Train).filter(Train.id == train_id).first()
            
            if not train:
                raise ValueError(f"Train with ID {train_id} not found")
            
            # Extract features
            features = self._extract_features_from_train(train)
            
            # Prepare features for prediction
            feature_array = self._prepare_features_for_prediction(features)
            
            # Predict
            probability = self.best_model.predict_proba(feature_array)[0][1]
            
            # Determine risk level
            if probability < 0.3:
                risk_level = "low"
                recommendation = "Safe for service - normal monitoring"
            elif probability < 0.6:
                risk_level = "medium" 
                recommendation = "Monitor closely - consider preventive maintenance"
            elif probability < 0.8:
                risk_level = "high"
                recommendation = "Schedule maintenance soon - increased failure risk"
            else:
                risk_level = "critical"
                recommendation = "Immediate maintenance required - high failure probability"
            
            failure_type = self._predict_failure_type(features, probability)
            
            return FailurePrediction(
                train_id=train.id,
                train_number=train.train_number,
                failure_probability=float(probability),
                risk_level=risk_level,
                predicted_failure_type=failure_type,
                confidence=float(probability),
                recommendation=recommendation,
                features=features,
                model_used=self.best_model_name,
                prediction_timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error predicting for train {train_id}: {e}")
            # Create fallback prediction
            return self._create_fallback_prediction(train)
    
    def _predict_failure_type(self, features: Dict, probability: float) -> str:
        """Predict the most likely failure type based on feature patterns"""
        if probability < 0.4:
            return None
        
        # Rule-based failure type prediction
        if features.get('maintenance_age_days', 0) > 180:
            return "Preventive Maintenance Overdue"
        elif features.get('open_jobs_count', 0) > 3:
            return "Mechanical Issues"
        elif features.get('mileage', 0) > 80000:
            return "High Mileage Component Wear"
        elif features.get('cert_validity_days', 0) < 7:
            return "Certification Compliance"
        elif features.get('mileage_per_year', 0) > 30000:
            return "High Utilization Stress"
        else:
            return "General Maintenance Required"
    
    def predict_all_trains(self) -> List[FailurePrediction]:
        """Predict failure risk for all active trains"""
        try:
            Train = self._get_train_model()
            trains = self.db.query(Train).filter(Train.status == "active").all()
            
            predictions = []
            for train in trains:
                try:
                    prediction = self.predict_failure_risk(train.id)
                    predictions.append(prediction)
                except Exception as e:
                    logger.error(f"Error predicting for train {train.id}: {e}")
                    # Create fallback prediction
                    predictions.append(self._create_fallback_prediction(train))
            
            return sorted(predictions, key=lambda x: x.failure_probability, reverse=True)
            
        except Exception as e:
            logger.error(f"Error predicting all trains: {e}")
            return []
    
    def _create_fallback_prediction(self, train) -> FailurePrediction:
        """Create a fallback prediction when model fails"""
        return FailurePrediction(
            train_id=train.id,
            train_number=train.train_number,
            failure_probability=0.5,
            risk_level="unknown",
            predicted_failure_type=None,
            confidence=0.0,
            recommendation="Error in prediction - manual inspection required",
            features={},
            model_used="fallback",
            prediction_timestamp=datetime.now()
        )
    
    def check_retraining_need(self) -> bool:
        """Check if model needs retraining based on time"""
        if not self.last_training_date:
            return True
        
        days_since = (datetime.now() - self.last_training_date).days
        needs_retraining = days_since >= self.auto_retrain_days
        
        if needs_retraining:
            logger.info(f"Model is {days_since} days old. Auto-retraining...")
            self.train_model()
        
        return needs_retraining
    
    def save_model(self):
        """Save trained model and preprocessing objects"""
        try:
            if self.best_model:
                model_data = {
                    'best_model': self.best_model,
                    'best_model_name': self.best_model_name,
                    'models': self.models,
                    'scaler': self.scaler,
                    'imputer': self.imputer,
                    'feature_names': self.feature_names,
                    'last_training_date': self.last_training_date,
                    'is_trained': self.is_trained
                }
                joblib.dump(model_data, self.model_dir / "failure_prediction_model.pkl")
                logger.info("Model saved successfully")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def load_model(self) -> bool:
        """Load trained model and preprocessing objects"""
        try:
            model_path = self.model_dir / "failure_prediction_model.pkl"
            if model_path.exists():
                model_data = joblib.load(model_path)
                
                self.best_model = model_data['best_model']
                self.best_model_name = model_data['best_model_name']
                self.models = model_data['models']
                self.scaler = model_data['scaler']
                self.imputer = model_data['imputer']
                self.feature_names = model_data['feature_names']
                self.last_training_date = model_data['last_training_date']
                self.is_trained = model_data.get('is_trained', True)
                
                logger.info("Model loaded successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "is_trained": self.is_trained,
            "best_model": self.best_model_name,
            "last_training": self.last_training_date.isoformat() if self.last_training_date else None,
            "auto_retrain_days": self.auto_retrain_days,
            "feature_count": len(self.feature_names) if self.feature_names else 0,
            "days_since_training": (datetime.now() - self.last_training_date).days if self.last_training_date else None
        }
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance from the best model"""
        if not self.is_trained or not self.best_model:
            return {}
        
        try:
            if hasattr(self.best_model, 'feature_importances_'):
                return dict(zip(self.feature_names, self.best_model.feature_importances_))
            return {}
        except:
            return {}

# Utility function to create the ML model instance
def create_ml_model(db: Session) -> MLModel:
    """Factory function to create ML model instance"""
    return MLModel(db)

if __name__ == "__main__":
    # Test the model
    from database import SessionLocal
    
    db = SessionLocal()
    try:
        ml_model = MLModel(db)
        
        # Get model info
        info = ml_model.get_model_info()
        print("Model Info:", info)
        
        # Make predictions if model is trained
        if ml_model.is_trained:
            predictions = ml_model.predict_all_trains()
            for pred in predictions[:5]:  # Show first 5
                print(f"Train {pred.train_number}: {pred.risk_level} risk ({pred.failure_probability:.3f}) - {pred.recommendation}")
        else:
            print("Model is not trained. Training now...")
            result = ml_model.train_model()
            print("Training result:", result)
            
    finally:
        db.close()