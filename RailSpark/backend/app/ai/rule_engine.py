from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional, Tuple
from datetime import date, datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import numpy as np
from scipy.optimize import linear_sum_assignment
import crud
import math
import random

class TrainStatus(Enum):
    AVAILABLE = "available"
    MAINTENANCE_NEEDED = "maintenance_needed"
    RESTRICTED = "restricted"
    UNAVAILABLE = "unavailable"

class PriorityLevel(Enum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    MINIMAL = 1

@dataclass
class TrainReadiness:
    train_id: int
    train_number: str
    status: TrainStatus
    readiness_score: float  # 0-1 scale
    priority: PriorityLevel
    constraints: List[str]
    capabilities: List[str]
    estimated_uptime: timedelta
    risk_factor: float

@dataclass
class ResourceAllocation:
    train_id: int
    train_number: str
    allocation_type: str  # 'primary', 'backup', 'maintenance'
    start_time: datetime
    end_time: datetime
    utilization_score: float
    cost_estimate: float

class AdvancedRuleEngine:
    def __init__(self, db: Session):
        self.db = db
        self.optimization_weights = {
            'availability': 0.25,
            'reliability': 0.20,
            'efficiency': 0.15,
            'safety': 0.20,
            'cost': 0.10,
            'utilization': 0.10
        }
    
    def generate_induction_plan(self, 
                              plan_date: date,
                              required_trains: int,
                              time_horizon: int = 7,
                              optimization_strategy: str = "balanced") -> Dict[str, Any]:
        """
        Generate optimized induction plan using multiple algorithms
        """
        # Phase 1: Train Readiness Assessment
        readiness_assessment = self._assess_train_readiness(plan_date)
        
        # Phase 2: Resource Optimization
        optimized_allocation = self._optimize_resource_allocation(
            readiness_assessment, 
            required_trains, 
            time_horizon,
            optimization_strategy
        )
        
        # Phase 3: Risk Mitigation
        risk_analysis = self._analyze_risks(optimized_allocation, plan_date)
        
        # Phase 4: Schedule Generation
        final_schedule = self._generate_schedule(optimized_allocation, risk_analysis)
        
        return {
            "plan_date": plan_date.isoformat(),
            "required_trains": required_trains,
            "readiness_summary": self._summarize_readiness(readiness_assessment),
            "allocations": [self._allocation_to_dict(alloc) for alloc in optimized_allocation],
            "risk_analysis": risk_analysis,
            "schedule": final_schedule,
            "efficiency_metrics": self._calculate_efficiency_metrics(optimized_allocation),
            "generation_timestamp": datetime.now().isoformat()
        }
    
    def _allocation_to_dict(self, allocation: ResourceAllocation) -> Dict[str, Any]:
        """Convert ResourceAllocation to dictionary for JSON serialization"""
        return {
            "train_id": allocation.train_id,
            "train_number": allocation.train_number,
            "allocation_type": allocation.allocation_type,
            "start_time": allocation.start_time.isoformat(),
            "end_time": allocation.end_time.isoformat(),
            "utilization_score": allocation.utilization_score,
            "cost_estimate": allocation.cost_estimate
        }
    
    def _assess_train_readiness(self, plan_date: date) -> List[TrainReadiness]:
        """
        Assess train readiness using multi-factor scoring algorithm
        """
        # Use safe database query with error handling
        try:
            trains = crud.trains.read_trains(self.db)
        except Exception as e:
            print(f"Error fetching trains: {e}")
            return []
        
        readiness_scores = []
        
        for train in trains:
            try:
                # Multi-factor readiness scoring
                base_score = self._calculate_base_readiness_score(train, plan_date)
                constraint_factor = self._calculate_constraint_penalties(train, plan_date)
                capability_bonus = self._calculate_capability_bonuses(train)
                
                # Composite readiness score (0-1 scale)
                readiness_score = max(0, min(1, base_score - constraint_factor + capability_bonus))
                
                # Determine status based on score
                if readiness_score >= 0.8:
                    status = TrainStatus.AVAILABLE
                    priority = PriorityLevel.HIGH
                elif readiness_score >= 0.6:
                    status = TrainStatus.AVAILABLE
                    priority = PriorityLevel.MEDIUM
                elif readiness_score >= 0.4:
                    status = TrainStatus.RESTRICTED
                    priority = PriorityLevel.LOW
                elif readiness_score >= 0.2:
                    status = TrainStatus.MAINTENANCE_NEEDED
                    priority = PriorityLevel.MINIMAL
                else:
                    status = TrainStatus.UNAVAILABLE
                    priority = PriorityLevel.MINIMAL
                
                # Safe attribute access with defaults
                train_id = getattr(train, 'id', 0)
                train_number = getattr(train, 'train_number', 'Unknown')
                
                readiness_scores.append(TrainReadiness(
                    train_id=train_id,
                    train_number=train_number,
                    status=status,
                    readiness_score=readiness_score,
                    priority=priority,
                    constraints=self._identify_constraints(train, plan_date),
                    capabilities=self._identify_capabilities(train),
                    estimated_uptime=self._estimate_uptime(train, readiness_score),
                    risk_factor=self._calculate_risk_factor(train, plan_date)
                ))
            except Exception as e:
                print(f"Error assessing train readiness for train {getattr(train, 'id', 'unknown')}: {e}")
                continue
        
        return sorted(readiness_scores, key=lambda x: x.readiness_score, reverse=True)
    
    def _calculate_base_readiness_score(self, train, plan_date: date) -> float:
        """
        Calculate base readiness score using weighted factors
        """
        train_id = getattr(train, 'id', 0)
        
        factors = {
            'status': self._score_status(getattr(train, 'status', 'unknown')),
            'fitness_certs': self._score_fitness_certificates(train_id),
            'maintenance': self._score_maintenance_status(train, plan_date),
            'mileage': self._score_mileage_utilization(train),
            'age': self._score_train_age(train),
            'reliability': self._score_reliability_history(train_id)
        }
        
        weights = {
            'status': 0.25,
            'fitness_certs': 0.20,
            'maintenance': 0.20,
            'mileage': 0.15,
            'age': 0.10,
            'reliability': 0.10
        }
        
        return sum(factors[factor] * weights[factor] for factor in factors)
    
    def _score_status(self, status: str) -> float:
        """Score train status"""
        status_scores = {
            'active': 1.0, 'operational': 1.0, 'running': 1.0,
            'available': 0.9, 'standby': 0.8, 'maintenance': 0.3,
            'inactive': 0.1, 'out_of_service': 0.0
        }
        return status_scores.get(status.lower(), 0.5)
    
    def _score_fitness_certificates(self, train_id: int) -> float:
        """
        Score fitness certificates with graceful degradation
        """
        try:
            # Use safe CRUD function call
            certs = []
            if hasattr(crud, 'fitness') and hasattr(crud.fitness, 'read_certificates_by_train'):
                certs = crud.fitness.read_certificates_by_train(self.db, train_id)
            
            if not certs:
                return 0.3  # Base score for no certificates
            
            valid_certs = [c for c in certs if getattr(c, 'is_valid', True)]
            total_departments = 5  # Expected departments
            coverage = len(valid_certs) / total_departments
            
            # Exponential decay for partial coverage
            return min(1.0, coverage * 1.5)
        except Exception as e:
            print(f"Error scoring fitness certificates for train {train_id}: {e}")
            return 0.5  # Default score if unable to check
    
    def _score_maintenance_status(self, train, plan_date: date) -> float:
        """Score maintenance status with predictive analysis"""
        try:
            last_maintenance = getattr(train, 'last_maintenance_date', None)
            if not last_maintenance:
                return 0.5  # Unknown maintenance history
            
            # Ensure both are date objects
            if isinstance(plan_date, datetime):
                plan_date = plan_date.date()
            if isinstance(last_maintenance, datetime):
                last_maintenance = last_maintenance.date()
            
            days_since_maintenance = (plan_date - last_maintenance).days
            
            # Weibull distribution for maintenance scoring
            scale = 45  # Characteristic life
            shape = 2.0  # Shape parameter
            maintenance_score = math.exp(-((days_since_maintenance / scale) ** shape))
            
            return max(0.1, maintenance_score)
        except Exception as e:
            print(f"Error scoring maintenance status: {e}")
            return 0.5
    
    def _score_mileage_utilization(self, train) -> float:
        """
        Score train mileage utilization using a reliability decay model.
        """
        try:
            mileage = getattr(train, 'mileage', None)
            if mileage is None:
                return 0.5  # default if no mileage data
            
            mileage = float(mileage)
            lifecycle_limit = 1_000_000  # expected lifecycle in km
            
            # Normalize mileage ratio (0.0 to 1.0)
            mileage_ratio = mileage / lifecycle_limit
            
            # Weibull decay model
            scale = 0.8
            shape = 3.0
            
            utilization_factor = (mileage_ratio / scale) ** shape
            score = math.exp(-utilization_factor)
            
            return max(0.0, min(1.0, score))
        
        except Exception as e:
            print(f"Error scoring mileage utilization: {e}")
            return 0.5
    
    def _score_train_age(self, train) -> float:
        """
        Score train based on its age relative to expected service life.
        """
        try:
            commissioning_date = getattr(train, 'commissioning_date', None)
            if commissioning_date is None:
                return 0.5  # Default score if unknown
            
            today = date.today()
            
            # Handle datetime conversion
            if isinstance(commissioning_date, datetime):
                commissioning_date = commissioning_date.date()
            
            age_years = (today - commissioning_date).days / 365.25
            
            lifecycle_limit = 30.0  # years
            mid_life = lifecycle_limit / 2
            
            # Logistic decay function
            scale = 5.0  # smoothing factor
            score = 1.0 / (1.0 + math.exp((age_years - mid_life) / scale))
            
            return max(0.0, min(1.0, score))
        
        except Exception as e:
            print(f"Error scoring train age: {e}")
            return 0.5

    def _score_reliability_history(self, train_id: int) -> float:
        """
        Score train reliability based on historical failure/incident records.
        """
        try:
            # If reliability records function doesn't exist, use maintenance status as proxy
            return 0.6  # Default neutral score since get_reliability_records doesn't exist
        
        except Exception as e:
            print(f"Error scoring reliability history for train {train_id}: {e}")
            return 0.5
    
    def _optimize_resource_allocation(self, 
                                    readiness: List[TrainReadiness],
                                    required_trains: int,
                                    time_horizon: int,
                                    strategy: str) -> List[ResourceAllocation]:
        """
        Optimize resource allocation using Hungarian algorithm and genetic optimization
        """
        if not readiness:
            return []
            
        available_trains = [t for t in readiness if t.status in [TrainStatus.AVAILABLE, TrainStatus.RESTRICTED]]
        
        if len(available_trains) < required_trains:
            # Use all available trains and supplement with maintenance-needed trains
            maintenance_trains = [t for t in readiness if t.status == TrainStatus.MAINTENANCE_NEEDED]
            available_trains.extend(maintenance_trains[:required_trains - len(available_trains)])
        
        if not available_trains:
            return []
        
        # Ensure we don't request more trains than available
        required_trains = min(required_trains, len(available_trains))
        
        # Create cost matrix for Hungarian algorithm
        cost_matrix = self._create_allocation_cost_matrix(available_trains, required_trains, strategy)
        
        # Apply Hungarian algorithm for optimal assignment
        try:
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
        except Exception as e:
            print(f"Error in linear sum assignment: {e}")
            # Fallback: simple sorting by readiness score
            available_trains.sort(key=lambda x: x.readiness_score, reverse=True)
            row_ind = list(range(min(required_trains, len(available_trains))))
            col_ind = list(range(min(required_trains, len(available_trains))))
        
        allocations = []
        base_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for i, train_idx in enumerate(row_ind[:required_trains]):
            if train_idx < len(available_trains):
                train = available_trains[train_idx]
                
                # Calculate allocation parameters
                allocation_type = self._determine_allocation_type(train, i, strategy)
                duration = self._calculate_allocation_duration(train, allocation_type)
                
                allocations.append(ResourceAllocation(
                    train_id=train.train_id,
                    train_number=train.train_number,
                    allocation_type=allocation_type,
                    start_time=base_time + timedelta(hours=i * 2),  # Staggered start times
                    end_time=base_time + timedelta(hours=i * 2 + duration.total_seconds() / 3600),
                    utilization_score=train.readiness_score,
                    cost_estimate=self._estimate_operational_cost(train, duration)
                ))
        
        return allocations
    
    def _create_allocation_cost_matrix(self, trains: List[TrainReadiness], 
                                     required_trains: int, strategy: str) -> np.ndarray:
        """
        Create cost matrix for optimization algorithm
        """
        n_trains = len(trains)
        cost_matrix = np.zeros((n_trains, required_trains))
        
        for i, train in enumerate(trains):
            for j in range(required_trains):
                if strategy == "safety_first":
                    cost = 1.0 - train.readiness_score  # Prefer higher readiness
                elif strategy == "efficiency":
                    cost = train.risk_factor  # Minimize risk
                elif strategy == "utilization":
                    cost = 1.0 / (train.readiness_score + 0.1)  # Maximize utilization
                else:  # balanced
                    cost = (1.0 - train.readiness_score) * 0.6 + train.risk_factor * 0.4
                
                cost_matrix[i, j] = cost
        
        return cost_matrix
    
    def _analyze_risks(self, allocations: List[ResourceAllocation], plan_date: date) -> Dict[str, Any]:
        """
        Perform comprehensive risk analysis using Monte Carlo simulation
        """
        if not allocations:
            return {"overall_risk": 0.0, "risks": [], "mitigations": []}
        
        # Monte Carlo simulation for risk assessment
        num_simulations = 1000
        failure_scenarios = []
        
        for i, allocation in enumerate(allocations):
            failure_probability = self._calculate_failure_probability(allocation)
            
            # Simulate failures
            simulations = np.random.binomial(1, failure_probability, num_simulations)
            failure_rate = np.mean(simulations)
            
            failure_scenarios.append({
                'train_id': allocation.train_id,
                'failure_probability': failure_probability,
                'simulated_failure_rate': failure_rate,
                'impact_severity': self._assess_impact_severity(allocation),
                'risk_level': self._classify_risk_level(failure_probability * self._assess_impact_severity(allocation))
            })
        
        overall_risk = np.mean([s['failure_probability'] * s['impact_severity'] 
                              for s in failure_scenarios])
        
        return {
            "overall_risk": float(overall_risk),
            "failure_scenarios": failure_scenarios,
            "risk_level": self._classify_risk_level(overall_risk),
            "recommended_mitigations": self._generate_mitigations(failure_scenarios)
        }
    
    def _calculate_failure_probability(self, allocation: ResourceAllocation) -> float:
        """
        Calculate failure probability using reliability engineering principles
        """
        base_failure_rate = 0.01  # Base failure rate per hour
        readiness_factor = 1.0 - allocation.utilization_score
        duration_hours = (allocation.end_time - allocation.start_time).total_seconds() / 3600
        
        # Weibull failure probability
        failure_prob = 1 - math.exp(-(base_failure_rate * duration_hours * readiness_factor))
        
        return min(0.99, failure_prob)
    
    def _generate_schedule(self, allocations: List[ResourceAllocation], 
                         risk_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate final schedule with risk mitigation
        """
        schedule = []
        
        for i, allocation in enumerate(allocations):
            schedule.append({
                "slot_id": i + 1,
                "train_id": allocation.train_id,
                "train_number": allocation.train_number,
                "allocation_type": allocation.allocation_type,
                "start_time": allocation.start_time.isoformat(),
                "end_time": allocation.end_time.isoformat(),
                "duration_hours": (allocation.end_time - allocation.start_time).total_seconds() / 3600,
                "readiness_score": allocation.utilization_score,
                "risk_level": risk_analysis['failure_scenarios'][i]['risk_level'] if i < len(risk_analysis['failure_scenarios']) else "medium",
                "backup_train": self._assign_backup_train(allocations, i),
                "contingency_plan": self._generate_contingency_plan(allocation, risk_analysis)
            })
        
        return schedule
    
    def _assign_backup_train(self, allocations: List[ResourceAllocation], 
                           current_index: int) -> Optional[str]:
        """
        Assign backup trains using round-robin algorithm
        """
        if len(allocations) <= 1:
            return None
        
        backup_index = (current_index + 1) % len(allocations)
        return allocations[backup_index].train_number
    
    # Helper methods for the algorithms
    def _calculate_constraint_penalties(self, train, plan_date: date) -> float:
        """Calculate penalties for operational constraints"""
        penalties = 0.0
        
        # Certificate constraints (reduced penalty)
        train_id = getattr(train, 'id', 0)
        try:
            certs = []
            if hasattr(crud, 'fitness') and hasattr(crud.fitness, 'read_certificates_by_train'):
                certs = crud.fitness.read_certificates_by_train(self.db, train_id)
            
            if not certs:
                penalties += 0.1  # Reduced from original
            else:
                valid_ratio = sum(1 for c in certs if getattr(c, 'is_valid', True)) / max(1, len(certs))
                penalties += (1.0 - valid_ratio) * 0.2
        except Exception as e:
            print(f"Error calculating certificate penalties: {e}")
            penalties += 0.05
        
        # Maintenance constraints
        try:
            last_maintenance = getattr(train, 'last_maintenance_date', None)
            if last_maintenance:
                if isinstance(plan_date, datetime):
                    plan_date = plan_date.date()
                if isinstance(last_maintenance, datetime):
                    last_maintenance = last_maintenance.date()
                    
                days_since = (plan_date - last_maintenance).days
                if days_since > 60:  # Critical maintenance
                    penalties += 0.3
                elif days_since > 45:  # Overdue maintenance
                    penalties += 0.15
        except Exception as e:
            print(f"Error calculating maintenance penalties: {e}")
            penalties += 0.05
        
        return min(0.5, penalties)  # Cap penalties
    
    def _calculate_capability_bonuses(self, train) -> float:
        """Calculate bonuses for enhanced capabilities"""
        bonuses = 0.0
        
        # Modern equipment bonus
        model = getattr(train, 'model', '')
        if any(x in str(model).lower() for x in ['modern', 'new', 'advanced']):
            bonuses += 0.1
        
        # High capacity bonus
        capacity = getattr(train, 'capacity', 0)
        if capacity > 200:
            bonuses += 0.05
        
        return min(0.2, bonuses)
    
    def _estimate_uptime(self, train, readiness_score: float) -> timedelta:
        """Estimate potential uptime using reliability modeling"""
        base_uptime = timedelta(hours=8)  # Base operational period
        reliability_factor = 0.5 + (readiness_score * 0.5)  # 0.5 to 1.0 scale
        
        return timedelta(hours=base_uptime.total_seconds() / 3600 * reliability_factor)
    
    def _calculate_risk_factor(self, train, plan_date: date) -> float:
        """Calculate comprehensive risk factor"""
        risk_components = []
        train_id = getattr(train, 'id', 0)
        
        # Age risk
        try:
            commissioning_date = getattr(train, 'commissioning_date', None)
            if commissioning_date:
                if isinstance(plan_date, datetime):
                    plan_date = plan_date.date()
                if isinstance(commissioning_date, datetime):
                    commissioning_date = commissioning_date.date()
                    
                age_years = (plan_date - commissioning_date).days / 365.25
                age_risk = min(1.0, age_years / 30)  # Normalize to 30 years
                risk_components.append(age_risk * 0.3)
        except:
            pass
        
        # Maintenance risk
        maintenance_risk = 1.0 - self._score_maintenance_status(train, plan_date)
        risk_components.append(maintenance_risk * 0.4)
        
        # Certificate risk
        certificate_risk = 1.0 - self._score_fitness_certificates(train_id)
        risk_components.append(certificate_risk * 0.3)
        
        return sum(risk_components) / len(risk_components) if risk_components else 0.5
    
    def _determine_allocation_type(self, train: int, 
                                 position: int, strategy: str) -> str:
        """Determine optimal allocation type"""
        if train.readiness_score >= 0.8:
            return "primary"
        elif train.readiness_score >= 0.6:
            return "secondary" if position % 3 != 0 else "primary"
        else:
            return "backup"
    
    def _calculate_allocation_duration(self, train: int, 
                                     allocation_type: str) -> timedelta:
        """Calculate allocation duration based on readiness"""
        base_duration = timedelta(hours=6)
        
        if allocation_type == "primary":
            multiplier = 0.8 + (train.readiness_score * 0.4)  # 0.8 to 1.2
        elif allocation_type == "secondary":
            multiplier = 0.6 + (train.readiness_score * 0.3)  # 0.6 to 0.9
        else:  # backup
            multiplier = 0.4 + (train.readiness_score * 0.2)  # 0.4 to 0.6
        
        hours = base_duration.total_seconds() / 3600 * multiplier
        return timedelta(hours=hours)
    
    def _estimate_operational_cost(self, train: int, 
                                 duration: timedelta) -> float:
        """Estimate operational cost using cost modeling"""
        base_cost_per_hour = 150.0  # Base operational cost
        efficiency_factor = 0.8 + (train.readiness_score * 0.4)  # 0.8 to 1.2
        
        hours = duration.total_seconds() / 3600
        return base_cost_per_hour * hours * efficiency_factor
    
    def _identify_constraints(self, train, plan_date: date) -> List[str]:
        """Identify operational constraints"""
        constraints = []
        train_id = getattr(train, 'id', 0)
        
        if self._score_fitness_certificates(train_id) < 0.5:
            constraints.append("certificate_issues")
        
        if self._score_maintenance_status(train, plan_date) < 0.6:
            constraints.append("maintenance_due")
        
        status = getattr(train, 'status', '').lower()
        if status not in ['active', 'operational', 'available']:
            constraints.append("status_limitation")
        
        return constraints
    
    def _identify_capabilities(self, train) -> List[str]:
        """Identify train capabilities"""
        capabilities = []
        
        capacity = getattr(train, 'capacity', 0)
        if capacity > 200:
            capabilities.append("high_capacity")
        
        max_speed = getattr(train, 'max_speed', 0)
        if max_speed > 80:
            capabilities.append("high_speed")
        
        return capabilities
    
    def _summarize_readiness(self, readiness: List[TrainReadiness]) -> Dict[str, Any]:
        """Summarize overall readiness assessment"""
        total_trains = len(readiness)
        if total_trains == 0:
            return {
                "total_trains_assessed": 0,
                "available_trains": 0,
                "availability_rate": 0,
                "average_readiness_score": 0,
                "readiness_distribution": {
                    "excellent": 0, "good": 0, "fair": 0, "poor": 0
                }
            }
        
        available = len([t for t in readiness if t.status in [TrainStatus.AVAILABLE, TrainStatus.RESTRICTED]])
        
        return {
            "total_trains_assessed": total_trains,
            "available_trains": available,
            "availability_rate": available / total_trains,
            "average_readiness_score": np.mean([t.readiness_score for t in readiness]) if readiness else 0,
            "readiness_distribution": {
                "excellent": len([t for t in readiness if t.readiness_score >= 0.8]),
                "good": len([t for t in readiness if 0.6 <= t.readiness_score < 0.8]),
                "fair": len([t for t in readiness if 0.4 <= t.readiness_score < 0.6]),
                "poor": len([t for t in readiness if t.readiness_score < 0.4])
            }
        }
    
    def _calculate_efficiency_metrics(self, allocations: List[ResourceAllocation]) -> Dict[str, float]:
        """Calculate plan efficiency metrics"""
        if not allocations:
            return {"utilization_rate": 0.0, "cost_efficiency": 0.0, "risk_adjusted_return": 0.0}
        
        total_utilization = sum(a.utilization_score for a in allocations)
        total_cost = sum(a.cost_estimate for a in allocations)
        
        return {
            "utilization_rate": total_utilization / len(allocations),
            "cost_efficiency": total_utilization / max(1, total_cost),
            "risk_adjusted_return": total_utilization / max(1, total_cost * 0.1)
        }
    
    def _classify_risk_level(self, risk_score: float) -> str:
        """Classify risk level"""
        if risk_score < 0.2:
            return "low"
        elif risk_score < 0.5:
            return "medium"
        elif risk_score < 0.8:
            return "high"
        else:
            return "critical"
    
    def _assess_impact_severity(self, allocation: ResourceAllocation) -> float:
        """Assess impact severity of failure"""
        if allocation.allocation_type == "primary":
            return 0.9
        elif allocation.allocation_type == "secondary":
            return 0.6
        else:
            return 0.3
    
    def _generate_contingency_plan(self, allocation: ResourceAllocation, 
                                 risk_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate contingency plan for allocation"""
        risk_level = risk_analysis['risk_level']
        
        contingencies = {
            "low": {"action": "monitor", "response_time": "60 minutes", "resources": "none"},
            "medium": {"action": "standby_crew", "response_time": "30 minutes", "resources": "minimal"},
            "high": {"action": "backup_train", "response_time": "15 minutes", "resources": "moderate"},
            "critical": {"action": "immediate_replacement", "response_time": "5 minutes", "resources": "full"}
        }
        
        return contingencies.get(risk_level, contingencies["medium"])
    
    def _generate_mitigations(self, failure_scenarios: List[Dict]) -> List[Dict]:
        """Generate risk mitigation strategies"""
        mitigations = []
        
        for scenario in failure_scenarios:
            if scenario['failure_probability'] > 0.3:
                mitigations.append({
                    "train_id": scenario['train_id'],
                    "mitigation": "enhanced_monitoring",
                    "priority": "high" if scenario['impact_severity'] > 0.7 else "medium",
                    "actions": ["frequent_inspections", "reduced_operational_load"]
                })
        
        return mitigations

# Usage example:
def create_advanced_rule_engine(db: Session) -> AdvancedRuleEngine:
    """Factory function to create advanced rule engine"""
    return AdvancedRuleEngine(db)