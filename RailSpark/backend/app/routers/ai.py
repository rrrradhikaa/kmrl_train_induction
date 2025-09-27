from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import date
from database import get_db
from ai.rule_engine import AdvancedRuleEngine, TrainReadiness
from ai.optimizer import InductionOptimizer, OptimizationResult, OptimizationConstraints
from ai.ml_model import MLModel, FailurePrediction
import schemas
import crud

router = APIRouter(prefix="/ai", tags=["ai services"])

@router.get("/eligibility", response_model=List[Dict[str, Any]])
def get_all_train_eligibility(db: Session = Depends(get_db)):
    """Get eligibility status for all trains"""
    rule_engine = AdvancedRuleEngine(db)
    eligibility_results = rule_engine._assess_train_readiness(plan_date=date.today())
    
    return [{
        "train_id": result.train_id,
        "train_number": result.train_number,
        "status": result.status.value,
        "readiness_score": result.readiness_score,
        "priority": result.priority.value,
        "constraints": result.constraints,
        "capabilities": result.capabilities,
        "estimated_uptime": result.estimated_uptime.total_seconds(),
        "risk_factor": result.risk_factor
    } for result in eligibility_results]

@router.get("/eligibility/{train_id}")
def get_train_eligibility(train_id: int, db: Session = Depends(get_db)):
    """Get eligibility status for a specific train"""
    rule_engine = AdvancedRuleEngine(db)
    try:
        eligibility_list = rule_engine._assess_train_readiness(plan_date=date.today())

        if not eligibility_list:
            raise HTTPException(status_code=404, detail=f"Train ID {train_id} not found")

        eligibility = eligibility_list[0]  # take the first element

        return {
            "train_id": eligibility.train_id,
            "train_number": eligibility.train_number,
            "status": eligibility.status.value,
            "readiness_score": eligibility.readiness_score,
            "priority": eligibility.priority.value,
            "constraints": eligibility.constraints,
            "capabilities": eligibility.capabilities,
            "estimated_uptime": eligibility.estimated_uptime.total_seconds(),
            "risk_factor": eligibility.risk_factor
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/generate-plan", response_model=List[Dict[str, Any]])
def generate_induction_plan(
    request_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Generate AI-optimized induction plan"""
    optimizer = InductionOptimizer(db)
    
    # Extract parameters from request body with proper validation
    plan_date_str = request_data.get('plan_date')
    constraints_data = request_data.get('constraints', {})
    
    # Convert string date to date object if provided
    plan_date = None
    if plan_date_str:
        try:
            if isinstance(plan_date_str, str):
                plan_date = date.fromisoformat(plan_date_str)
            else:
                raise HTTPException(
                    status_code=400, 
                    detail="plan_date must be a string in ISO format (YYYY-MM-DD)"
                )
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="Invalid date format. Use YYYY-MM-DD"
            )
    
    # Create constraints object with proper validation
    opt_constraints = None
    if constraints_data:
        try:
            # Validate and convert constraint values to appropriate types
            validated_constraints = {}
            
            # Max trains constraint
            if 'max_trains' in constraints_data:
                max_trains = constraints_data['max_trains']
                if isinstance(max_trains, int) and max_trains > 0:
                    validated_constraints['max_trains'] = max_trains
                else:
                    raise ValueError("max_trains must be a positive integer")
            
            # Priority trains constraint
            if 'priority_trains' in constraints_data:
                priority_trains = constraints_data['priority_trains']
                if isinstance(priority_trains, list):
                    validated_constraints['priority_trains'] = [
                        int(train_id) for train_id in priority_trains
                    ]
                else:
                    raise ValueError("priority_trains must be a list of train IDs")
            
            # Maintenance threshold constraint
            if 'maintenance_threshold' in constraints_data:
                threshold = constraints_data['maintenance_threshold']
                if isinstance(threshold, (int, float)) and threshold >= 0:
                    validated_constraints['maintenance_threshold'] = float(threshold)
                else:
                    raise ValueError("maintenance_threshold must be a non-negative number")
            
            # Available only constraint
            if 'available_only' in constraints_data:
                available_only = constraints_data['available_only']
                if isinstance(available_only, bool):
                    validated_constraints['available_only'] = available_only
                else:
                    raise ValueError("available_only must be a boolean")
            
            opt_constraints = OptimizationConstraints(**validated_constraints)
            
        except (ValueError, TypeError) as e:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid constraints format: {str(e)}"
            )
    
    try:
        # Generate the induction plan with proper error handling
        induction_plan = optimizer.generate_induction_plan(plan_date, opt_constraints)
        
        # Ensure the response is properly serializable
        if not induction_plan:
            return []
        
        # Convert the plan to a JSON-serializable format
        serializable_plan = []
        for plan_item in induction_plan:
            if isinstance(plan_item, dict):
                serializable_plan.append(plan_item)
            else:
                # If it's an object, convert to dict
                serializable_plan.append({
                    key: getattr(plan_item, key) for key in dir(plan_item) 
                    if not key.startswith('_') and not callable(getattr(plan_item, key))
                })
        
        return serializable_plan
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log the actual error for debugging
        print(f"Error generating induction plan: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Internal server error while generating induction plan"
        )

@router.get("/failure-predictions", response_model=List[Dict[str, Any]])
def get_failure_predictions(db: Session = Depends(get_db)):
    """Get failure predictions for all trains"""
    ml_model = MLModel(db)
    
    try:
        if not ml_model.is_trained:
            # Train model if not already trained
            training_result = ml_model.train_model()
            if not training_result["success"]:
                raise HTTPException(
                    status_code=400, 
                    detail="Model training failed: " + training_result.get("message", "Unknown error")
                )
        
        predictions = ml_model.predict_all_trains()
        
        return [{
            "train_id": pred.train_id,
            "train_number": pred.train_number,
            "failure_probability": pred.failure_probability,
            "risk_level": pred.risk_level,
            "predicted_failure_type": pred.predicted_failure_type,
            "confidence": pred.confidence,
            "recommendation": pred.recommendation,
            "features": pred.features
        } for pred in predictions]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.get("/failure-predictions/{train_id}")
def get_train_failure_prediction(train_id: int, db: Session = Depends(get_db)):
    """Get failure prediction for a specific train"""
    ml_model = MLModel(db)
    
    try:
        if not ml_model.is_trained:
            training_result = ml_model.train_model()
            if not training_result["success"]:
                raise HTTPException(
                    status_code=400, 
                    detail="Model training failed"
                )
        
        prediction = ml_model.predict_failure_risk(train_id)
        
        return {
            "train_id": prediction.train_id,
            "train_number": prediction.train_number,
            "failure_probability": prediction.failure_probability,
            "risk_level": prediction.risk_level,
            "predicted_failure_type": prediction.predicted_failure_type,
            "confidence": prediction.confidence,
            "recommendation": prediction.recommendation,
            "features": prediction.features
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/train-model")
def train_ml_model(db: Session = Depends(get_db)):
    """Train or retrain the ML model"""
    ml_model = MLModel(db)
    
    try:
        result = ml_model.train_model()
        return {
            "success": result["success"],
            "accuracy": result.get("accuracy"),
            "training_samples": result.get("training_samples"),
            "test_samples": result.get("test_samples"),
            "feature_importance": result.get("feature_importance")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/optimization-stats")
def get_optimization_statistics(db: Session = Depends(get_db)):
    """Get statistics for optimization analysis"""
    rule_engine = AdvancedRuleEngine(db)
    optimizer = InductionOptimizer(db)
    
    # Basic statistics
    total_trains = len(crud.trains.read_trains(db))
    active_trains = len(crud.trains.read_active_trains(db))
    eligible_trains = len(rule_engine._assess_train_readiness(plan_date=date.today()))
    
    # Generate sample plan for analysis
    try:
        sample_plan = optimizer.generate_induction_plan()
        service_trains = len([p for p in sample_plan if p['induction_type'] == 'service'])
        standby_trains = len([p for p in sample_plan if p['induction_type'] == 'standby'])
        maintenance_trains = len([p for p in sample_plan if p['induction_type'] == 'maintenance'])
    except Exception:
        service_trains = standby_trains = maintenance_trains = 0
    
    return {
        "total_trains": total_trains,
        "active_trains": active_trains,
        "eligible_trains": eligible_trains,
        "planned_service_trains": service_trains,
        "planned_standby_trains": standby_trains,
        "planned_maintenance_trains": maintenance_trains,
        "utilization_rate": eligible_trains / active_trains if active_trains > 0 else 0
    }