from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional, Tuple
from datetime import date, datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import crud
from .rule_engine import AdvancedRuleEngine
import numpy as np
from ortools.linear_solver import pywraplp
import logging

logger = logging.getLogger(__name__)

class InductionType(Enum):
    SERVICE = "service"
    STANDBY = "standby"
    MAINTENANCE = "maintenance"

@dataclass
class OptimizationResult:
    train_id: int
    train_number: str
    induction_type: InductionType
    rank: int
    score: float
    reasons: List[str]
    metadata: Dict[str, Any]

@dataclass
class OptimizationConstraints:
    min_service_trains: int = 15
    max_service_trains: int = 20
    min_standby_trains: int = 3
    max_standby_trains: int = 5
    target_branding_exposure: float = 0.8  # 80% of required exposure
    max_mileage_variance: float = 0.2  # 20% variance allowed
    plan_date: Optional[date] = None
    # New constraints for advanced optimization
    max_maintenance_trains: int = 10
    service_weight: float = 0.6
    standby_weight: float = 0.25
    maintenance_weight: float = 0.15

class InductionOptimizer:
    def __init__(self, db: Session):
        self.db = db
        self.rule_engine = AdvancedRuleEngine(db)
        self.solver = None
    
    def optimize_induction_plan(self, plan_date: date = None, 
                          constraints: OptimizationConstraints = None) -> List[OptimizationResult]:
        """Generate optimized induction plan using MILP optimization"""
        if plan_date is None:
            plan_date = date.today() + timedelta(days=1)
        
        if constraints is None:
            constraints = OptimizationConstraints()
            constraints.plan_date = plan_date
        
        logger.info(f"Starting optimization for date: {plan_date}")
        
        # FIXED: Get eligible trains correctly
        readiness_results = self.rule_engine._assess_train_readiness(plan_date=date.today())
        
        if not readiness_results:
            raise ValueError("No eligible trains found for induction planning")
        
        # Extract train IDs from TrainReadiness objects
        train_ids = [result.train_id for result in readiness_results]
        
        # Query actual train objects from database
        eligible_trains = []
        for train_id in train_ids:
            try:
                train = crud.trains.read_train(self.db, train_id)
                if train:
                    eligible_trains.append(train)
            except Exception as e:
                logger.warning(f"Could not load train {train_id}: {e}")
        
        if not eligible_trains:
            raise ValueError("No valid trains found for induction planning")
        
        logger.info(f"Found {len(eligible_trains)} eligible trains")
        
        # Step 2: Calculate comprehensive scores for each train
        train_scores = self._calculate_train_scores(eligible_trains, plan_date)
        
        # Step 3: Apply MILP optimization with constraints
        optimized_plan = self._apply_milp_optimization(
            eligible_trains, train_scores, constraints
        )
        
        logger.info(f"Optimization completed. Generated plan with {len(optimized_plan)} assignments")
        return optimized_plan
    
    def _calculate_train_scores(self, trains: List, plan_date: date) -> Dict[int, Dict[str, float]]:
        """Calculate multiple scoring factors for each train using advanced algorithms"""
        scores = {}
        
        # Pre-calculate fleet statistics for normalization
        fleet_stats = self._calculate_fleet_statistics(trains)
        
        for train in trains:
            try:
                # Calculate individual factor scores with advanced algorithms
                mileage_score = self._calculate_advanced_mileage_score(train, fleet_stats)
                branding_score = self._calculate_advanced_branding_score(train, plan_date)
                maintenance_score = self._calculate_advanced_maintenance_score(train, plan_date)
                cleaning_score = self._calculate_advanced_cleaning_score(train, plan_date)
                stabling_score = self._calculate_advanced_stabling_score(train)
                historical_score = self._calculate_advanced_historical_score(train, plan_date)
                operational_score = self._calculate_operational_readiness_score(train)
                
                train_scores = {
                    'mileage_score': mileage_score,
                    'branding_score': branding_score,
                    'maintenance_score': maintenance_score,
                    'cleaning_score': cleaning_score,
                    'stabling_score': stabling_score,
                    'historical_score': historical_score,
                    'operational_score': operational_score
                }
                
                # Dynamic weighting based on business rules
                weights = self._calculate_dynamic_weights(train, plan_date, train_scores)
                
                # Normalize scores and calculate weighted combination
                normalized_scores = self._normalize_scores(train_scores)
                combined_score = sum(normalized_scores[factor] * weights[factor] 
                                   for factor in normalized_scores)
                
                scores[train.id] = {
                    'scores': train_scores,
                    'normalized_scores': normalized_scores,
                    'combined_score': combined_score,
                    'weights': weights,
                    'factors': train_scores
                }
                
            except Exception as e:
                logger.error(f"Error calculating scores for train {train.id}: {e}")
                # Assign default scores in case of error
                scores[train.id] = self._get_default_scores()
        
        return scores
    
    def _calculate_fleet_statistics(self, trains: List) -> Dict[str, float]:
        """Calculate fleet-wide statistics for normalization"""
        if not trains:
            return {}
        
        mileages = [t.current_mileage for t in trains if t.current_mileage is not None]
        maintenance_dates = [t.last_maintenance_date for t in trains if t.last_maintenance_date is not None]
        
        return {
            'avg_mileage': np.mean(mileages) if mileages else 0,
            'std_mileage': np.std(mileages) if mileages else 1,
            'min_mileage': min(mileages) if mileages else 0,
            'max_mileage': max(mileages) if mileages else 0,
            'avg_days_since_maintenance': np.mean([(date.today() - d).days for d in maintenance_dates]) if maintenance_dates else 0
        }
    
    def _calculate_advanced_mileage_score(self, train, fleet_stats: Dict) -> float:
        """Advanced mileage scoring using z-score normalization"""
        if not train.current_mileage or fleet_stats['std_mileage'] == 0:
            return 0.5
        
        # Calculate z-score (how many standard deviations from mean)
        z_score = (train.current_mileage - fleet_stats['avg_mileage']) / fleet_stats['std_mileage']
        
        # Convert to score: lower mileage = higher score, with normal distribution
        # Using cumulative distribution function approximation
        mileage_score = 1 - (1 / (1 + np.exp(-z_score)))
        
        return max(0.1, min(0.9, mileage_score))
    
    def _calculate_advanced_branding_score(self, train, plan_date: date) -> float:
        """Advanced branding exposure scoring with contract prioritization"""
        active_contracts = crud.branding.read_active_contracts(self.db, train.id)
        if not active_contracts:
            return 0.3  # Lower priority for trains without branding
        
        total_weighted_score = 0
        total_weight = 0
        
        for contract in active_contracts:
            # Calculate exposure deficit
            exposure_ratio = contract.exposure_hours_fulfilled / max(contract.exposure_hours_required, 1)
            days_remaining = (contract.end_date - plan_date).days
            
            # Priority factors: exposure deficit, contract value, urgency
            exposure_deficit = 1 - exposure_ratio
            urgency_factor = 1 / max(days_remaining, 1)  # Higher urgency for closer end dates
            value_factor = min(contract.contract_value / 100000, 1) if contract.contract_value else 0.5
            
            contract_weight = exposure_deficit * urgency_factor * value_factor
            contract_score = exposure_deficit  # Higher score for greater deficit
            
            total_weighted_score += contract_score * contract_weight
            total_weight += contract_weight
        
        if total_weight == 0:
            return 0.5
        
        return max(0.1, min(0.9, total_weighted_score / total_weight))
    
    def _calculate_advanced_maintenance_score(self, train, plan_date: date) -> float:
        """Advanced maintenance scoring with predictive analysis"""
        if not train.last_maintenance_date:
            return 0.8  # Higher score for trains needing first maintenance
        
        days_since_maintenance = (plan_date - train.last_maintenance_date).days
        maintenance_interval = train.maintenance_interval or 30  # Default 30 days
        
        # Calculate how close to next maintenance (0 = just maintained, 1 = overdue)
        maintenance_urgency = min(days_since_maintenance / maintenance_interval, 1.5) / 1.5
        
        # Inverse score: higher urgency = lower operational score
        maintenance_score = 1 - maintenance_urgency
        
        return max(0.1, min(0.9, maintenance_score))
    
    def _calculate_advanced_cleaning_score(self, train, plan_date: date) -> float:
        """Advanced cleaning schedule scoring"""
        cleaning_slots = crud.cleaning.read_slots_by_train(self.db, train.id)
        
        if not cleaning_slots:
            return 0.3  # Lower score if no cleaning history
        
        # Find most recent completed cleaning
        recent_cleanings = [
            slot for slot in cleaning_slots 
            if slot.status == "completed" and slot.slot_time.date() <= plan_date
        ]
        
        if not recent_cleanings:
            return 0.3
        
        latest_cleaning = max(recent_cleanings, key=lambda x: x.slot_time)
        days_since_cleaning = (plan_date - latest_cleaning.slot_time.date()).days
        
        # Exponential decay: score decreases as time since cleaning increases
        cleaning_score = np.exp(-days_since_cleaning / 7)  # Half-life of 7 days
        
        return max(0.1, min(0.9, cleaning_score))
    
    def _calculate_advanced_stabling_score(self, train) -> float:
        """Advanced stabling position optimization"""
        stabling_info = crud.stabling.read_geometry_by_train(self.db, train.id)
        if not stabling_info:
            return 0.5
        
        # Multi-factor stabling score
        factors = []
        
        # Shunting requirement penalty
        if stabling_info.shunting_required:
            factors.append(0.3)
        else:
            factors.append(0.9)
        
        # Distance from service entry point
        if hasattr(stabling_info, 'distance_to_entry'):
            distance_score = max(0.1, 1 - (stabling_info.distance_to_entry / 1000))  # Normalize by 1km
            factors.append(distance_score)
        
        # Track accessibility
        if hasattr(stabling_info, 'accessibility_score'):
            factors.append(stabling_info.accessibility_score)
        
        return np.mean(factors) if factors else 0.5
    
    def _calculate_advanced_historical_score(self, train, plan_date: date) -> float:
        """Advanced historical performance scoring"""
        try:
            # Get historical performance data - this returns a dictionary, not an iterable object
            historical_data = crud.get_train_performance_history(self.db, train.id, 30)  # Last 30 days
            
            if not historical_data:
                return 0.7
            
            # FIX: Check if historical_data is a dictionary with the expected structure
            if isinstance(historical_data, dict):
                # Use the dictionary keys that we know exist
                on_time_performance = historical_data.get('on_time', 0.9)
                reliability = historical_data.get('reliability', 0.9)
                availability = historical_data.get('availability', 0.9)
                
                # Calculate historical score using available metrics
                historical_score = (on_time_performance * 0.4 + 
                                reliability * 0.4 + 
                                availability * 0.2)
                
                return max(0.1, min(0.9, historical_score))
            else:
                # Fallback for unexpected data type
                logger.warning(f"Unexpected historical data type for train {train.id}: {type(historical_data)}")
                return 0.7
                
        except Exception as e:
            logger.warning(f"Could not calculate historical score for train {train.id}: {e}")
            return 0.7
    
    def _calculate_operational_readiness_score(self, train) -> float:
        """Calculate overall operational readiness"""
        # Check various operational factors
        factors = []
        
        # Equipment status
        if train.equipment_status == "operational":
            factors.append(0.9)
        elif train.equipment_status == "maintenance":
            factors.append(0.3)
        else:
            factors.append(0.6)
        
        # Crew availability (simplified) - FIX: Handle dictionary return type
        try:
            crew_data = crud.get_crew_availability(self.db, date.today())  # Use current date
            if isinstance(crew_data, dict):
                utilization_rate = crew_data.get('utilization_rate', 0.5)
                factors.append(utilization_rate)
            else:
                factors.append(0.5)  # Default if data format is unexpected
        except Exception as e:
            logger.warning(f"Could not get crew availability for train {train.id}: {e}")
            factors.append(0.5)
        
        # Fuel/energy status (if available)
        if hasattr(train, 'fuel_level') and train.fuel_level > 0.5:
            factors.append(0.9)
        else:
            factors.append(0.3)
        
        return np.mean(factors) if factors else 0.6
    
    def _calculate_dynamic_weights(self, train, plan_date: date, scores: Dict) -> Dict[str, float]:
        """Calculate dynamic weights based on current conditions and priorities"""
        base_weights = {
            'mileage_score': 0.20,
            'branding_score': 0.15,
            'maintenance_score': 0.15,
            'cleaning_score': 0.10,
            'stabling_score': 0.10,
            'historical_score': 0.10,
            'operational_score': 0.20
        }
        
        # Adjust weights based on day of week, season, or other factors
        day_of_week = plan_date.weekday()
        
        # Higher maintenance priority on weekends
        if day_of_week >= 5:  # weekend
            base_weights['maintenance_score'] += 0.05
            base_weights['cleaning_score'] += 0.05
        
        # Normalize weights to sum to 1
        total = sum(base_weights.values())
        normalized_weights = {k: v/total for k, v in base_weights.items()}
        
        return normalized_weights
    
    def _normalize_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Normalize scores to consistent scale"""
        # Simple min-max normalization to [0.1, 0.9] range
        normalized = {}
        min_val = min(scores.values())
        max_val = max(scores.values())
        
        if max_val == min_val:
            return {k: 0.5 for k in scores.keys()}
        
        for factor, score in scores.items():
            normalized_score = 0.1 + 0.8 * (score - min_val) / (max_val - min_val)
            normalized[factor] = normalized_score
        
        return normalized
    
    def _get_default_scores(self) -> Dict:
        """Return default scores for error handling"""
        return {
            'scores': {},
            'normalized_scores': {},
            'combined_score': 0.5,
            'weights': {},
            'factors': {}
        }
    
    def _apply_milp_optimization(self, trains: List, scores: Dict, 
                               constraints: OptimizationConstraints) -> List[OptimizationResult]:
        """Apply Mixed Integer Linear Programming optimization"""
        
        # Create solver
        solver = pywraplp.Solver.CreateSolver('SCIP')
        if not solver:
            raise RuntimeError("Could not create solver")
        
        n_trains = len(trains)
        n_types = 3  # SERVICE, STANDBY, MAINTENANCE
        
        # Decision variables: x[i][j] = 1 if train i is assigned to type j
        x = {}
        for i in range(n_trains):
            for j in range(n_types):
                x[i, j] = solver.IntVar(0, 1, f'x_{i}_{j}')
        
        # Objective: Maximize total score
        objective = solver.Objective()
        for i in range(n_trains):
            train = trains[i]
            train_score = scores[train.id]['combined_score']
            
            # Different weights for different assignment types
            service_score = train_score * constraints.service_weight
            standby_score = train_score * constraints.standby_weight
            maintenance_score = (1 - train_score) * constraints.maintenance_weight  # Lower operational score = higher maintenance priority
            
            objective.SetCoefficient(x[i, 0], service_score)      # SERVICE
            objective.SetCoefficient(x[i, 1], standby_score)      # STANDBY
            objective.SetCoefficient(x[i, 2], maintenance_score)  # MAINTENANCE
        
        objective.SetMaximization()
        
        # Constraints
        
        # Each train assigned to exactly one type
        for i in range(n_trains):
            constraint = solver.Constraint(1, 1)
            for j in range(n_types):
                constraint.SetCoefficient(x[i, j], 1)
        
        # Service train count constraints
        service_constraint = solver.Constraint(constraints.min_service_trains, 
                                             constraints.max_service_trains)
        for i in range(n_trains):
            service_constraint.SetCoefficient(x[i, 0], 1)
        
        # Standby train count constraints
        standby_constraint = solver.Constraint(constraints.min_standby_trains,
                                            constraints.max_standby_trains)
        for i in range(n_trains):
            standby_constraint.SetCoefficient(x[i, 1], 1)
        
        # Maintenance train count constraint
        maintenance_constraint = solver.Constraint(0, constraints.max_maintenance_trains)
        for i in range(n_trains):
            maintenance_constraint.SetCoefficient(x[i, 2], 1)
        
        # Additional constraints for operational requirements
        
        # Branding exposure constraint (simplified)
        branding_trains = []
        for i in range(n_trains):
            train = trains[i]
            branding_score = scores[train.id]['scores']['branding_score']
            if branding_score > 0.7:  # High branding priority
                branding_trains.append(i)
        
        if branding_trains:
            min_branding = max(1, int(len(branding_trains) * constraints.target_branding_exposure))
            branding_constraint = solver.Constraint(min_branding, len(branding_trains))
            for i in branding_trains:
                branding_constraint.SetCoefficient(x[i, 0], 1)  # Assign to service
        
        # Solve the problem
        status = solver.Solve()
        
        if status != pywraplp.Solver.OPTIMAL:
            logger.warning("MILP optimization failed, falling back to heuristic method")
            return self._apply_heuristic_optimization(trains, scores, constraints)
        
        # Extract results
        results = []
        assignment_rank = 1
        
        # Create assignments based on MILP solution
        for i in range(n_trains):
            for j in range(n_types):
                if x[i, j].solution_value() > 0.5:  # Assignment found
                    train = trains[i]
                    train_score = scores[train.id]['combined_score']
                    
                    if j == 0:
                        induction_type = InductionType.SERVICE
                        reasons = ["Optimized service assignment"]
                    elif j == 1:
                        induction_type = InductionType.STANDBY
                        reasons = ["Optimized standby assignment"]
                    else:
                        induction_type = InductionType.MAINTENANCE
                        reasons = ["Scheduled for maintenance"]
                    
                    result = OptimizationResult(
                        train_id=train.id,
                        train_number=train.train_number,
                        induction_type=induction_type,
                        rank=assignment_rank,
                        score=train_score,
                        reasons=reasons,
                        metadata=scores[train.id]['factors']
                    )
                    results.append(result)
                    assignment_rank += 1
                    break
        
        return results
    
    def _apply_heuristic_optimization(self, trains: List, scores: Dict,
                                    constraints: OptimizationConstraints) -> List[OptimizationResult]:
        """Fallback heuristic optimization when MILP fails"""
        
        # Sort trains by combined score (descending)
        sorted_trains = sorted(trains, key=lambda t: scores[t.id]['combined_score'], reverse=True)
        
        results = []
        service_count = 0
        standby_count = 0
        maintenance_count = 0
        
        # Phase 1: Assign mandatory service trains (highest scores)
        for train in sorted_trains:
            if service_count < constraints.min_service_trains:
                results.append(self._create_result(train, scores, InductionType.SERVICE, 
                                                 "Minimum service requirement"))
                service_count += 1
        
        # Phase 2: Assign optimal service trains
        for train in sorted_trains:
            if train.id in [r.train_id for r in results]:
                continue  # Skip already assigned trains
                
            if (service_count < constraints.max_service_trains and 
                scores[train.id]['combined_score'] > 0.6):
                results.append(self._create_result(train, scores, InductionType.SERVICE,
                                                 "High optimization score"))
                service_count += 1
        
        # Phase 3: Assign standby trains
        for train in sorted_trains:
            if train.id in [r.train_id for r in results]:
                continue
                
            if standby_count < constraints.max_standby_trains:
                results.append(self._create_result(train, scores, InductionType.STANDBY,
                                                 "Standby assignment"))
                standby_count += 1
        
        # Phase 4: Assign remaining trains to maintenance
        for train in sorted_trains:
            if train.id in [r.train_id for r in results]:
                continue
                
            if maintenance_count < constraints.max_maintenance_trains:
                results.append(self._create_result(train, scores, InductionType.MAINTENANCE,
                                                 "Maintenance scheduling"))
                maintenance_count += 1
        
        # Assign ranks based on service priority then score
        service_trains = [r for r in results if r.induction_type == InductionType.SERVICE]
        standby_trains = [r for r in results if r.induction_type == InductionType.STANDBY]
        maintenance_trains = [r for r in results if r.induction_type == InductionType.MAINTENANCE]
        
        service_trains.sort(key=lambda x: x.score, reverse=True)
        standby_trains.sort(key=lambda x: x.score, reverse=True)
        maintenance_trains.sort(key=lambda x: x.score)  # Lower score = higher maintenance priority
        
        ranked_results = service_trains + standby_trains + maintenance_trains
        for i, result in enumerate(ranked_results):
            result.rank = i + 1
        
        return ranked_results
    
    def _create_result(self, train, scores: Dict, induction_type: InductionType, 
                      reason: str) -> OptimizationResult:
        """Helper method to create OptimizationResult"""
        return OptimizationResult(
            train_id=train.id,
            train_number=train.train_number,
            induction_type=induction_type,
            rank=0,  # Will be assigned later
            score=scores[train.id]['combined_score'],
            reasons=[reason],
            metadata=scores[train.id]['factors']
        )
    
    def generate_induction_plan(self, plan_date: date = None, constraints: OptimizationConstraints = None) -> List[Dict[str, Any]]:
        """Generate final induction plan ready for database storage"""
        try:
            # Use the provided plan_date or default to tomorrow
            target_date = plan_date or (date.today() + timedelta(days=1))
            
            # Get optimized results
            optimized_results = self.optimize_induction_plan(target_date, constraints)
            
            induction_plans = []
            for result in optimized_results:
                plan = {
                    'train_id': result.train_id,
                    'train_number': result.train_number,  # Include train_number for clarity
                    'plan_date': target_date.isoformat(),  # Convert to string for JSON serialization
                    'induction_type': result.induction_type.value,
                    'rank': result.rank,
                    'reason': '; '.join(result.reasons),
                    'score': float(result.score),  # Ensure it's a float for JSON
                    'metadata': result.metadata,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                induction_plans.append(plan)
            
            logger.info(f"Generated induction plan with {len(induction_plans)} assignments for date {target_date}")
            return induction_plans
            
        except Exception as e:
            logger.error(f"Error generating induction plan: {str(e)}")
            raise ValueError(f"Failed to generate induction plan: {str(e)}")
    
    def validate_optimization_result(self, results: List[OptimizationResult], 
                                   constraints: OptimizationConstraints) -> Dict[str, Any]:
        """Validate the optimization result against constraints"""
        validation_result = {
            'is_valid': True,
            'violations': [],
            'summary': {}
        }
        
        service_count = sum(1 for r in results if r.induction_type == InductionType.SERVICE)
        standby_count = sum(1 for r in results if r.induction_type == InductionType.STANDBY)
        maintenance_count = sum(1 for r in results if r.induction_type == InductionType.MAINTENANCE)
        
        validation_result['summary'] = {
            'service_trains': service_count,
            'standby_trains': standby_count,
            'maintenance_trains': maintenance_count,
            'total_trains': len(results)
        }
        
        # Check constraints
        if service_count < constraints.min_service_trains:
            validation_result['violations'].append(
                f"Service trains ({service_count}) below minimum ({constraints.min_service_trains})"
            )
        if service_count > constraints.max_service_trains:
            validation_result['violations'].append(
                f"Service trains ({service_count}) above maximum ({constraints.max_service_trains})"
            )
        if standby_count < constraints.min_standby_trains:
            validation_result['violations'].append(
                f"Standby trains ({standby_count}) below minimum ({constraints.min_standby_trains})"
            )
        if standby_count > constraints.max_standby_trains:
            validation_result['violations'].append(
                f"Standby trains ({standby_count}) above maximum ({constraints.max_standby_trains})"
            )
        if maintenance_count > constraints.max_maintenance_trains:
            validation_result['violations'].append(
                f"Maintenance trains ({maintenance_count}) above maximum ({constraints.max_maintenance_trains})"
            )
        
        validation_result['is_valid'] = len(validation_result['violations']) == 0
        
        return validation_result