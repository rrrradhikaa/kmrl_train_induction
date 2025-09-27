from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import date, datetime, timedelta
from database import get_db
from ai.rule_engine import AdvancedRuleEngine, TrainStatus
from ai.optimizer import InductionOptimizer
from ai.ml_model import MLModel

# Import specific CRUD functions instead of the whole module
from crud.trains import read_trains, read_active_trains, read_train
from crud.job_cards import read_open_job_cards
from crud.branding import read_active_contracts, read_contracts_need_exposure
from crud.induction import read_todays_plan

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/overview")
def get_dashboard_overview(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get dashboard overview statistics"""
    try:
        # Basic counts - use the imported functions directly
        all_trains = read_trains(db)
        total_trains = len(all_trains)
        active_trains_list = read_active_trains(db)
        active_trains = len(active_trains_list)
        
        # Eligibility status - Fixed method call
        rule_engine = AdvancedRuleEngine(db)
        readiness_assessment = rule_engine._assess_train_readiness(date.today())
        eligible_trains = len([t for t in readiness_assessment if t.status in [TrainStatus.AVAILABLE, TrainStatus.RESTRICTED]])
        
        # Maintenance status
        open_jobs = read_open_job_cards(db)
        trains_with_open_jobs = len(set(job.train_id for job in open_jobs))
        
        # Branding status
        active_contracts_list = read_active_contracts(db)
        contracts_needing_exposure = len(read_contracts_need_exposure(db))
        
        # Today's induction plan
        todays_plan_list = read_todays_plan(db)
        service_trains = len([p for p in todays_plan_list if p.induction_type == 'service'])
        standby_trains = len([p for p in todays_plan_list if p.induction_type == 'standby'])
        
        # Failure predictions (sample)
        ml_model = MLModel(db)
        high_risk_trains = 0
        try:
            if ml_model.is_trained:
                predictions = ml_model.predict_all_trains()
                high_risk_trains = len([p for p in predictions if p.risk_level == "high"])
        except:
            pass  # Ignore prediction errors in overview
        
        return {
            "summary": {
                "total_trains": total_trains,
                "active_trains": active_trains,
                "eligible_trains": eligible_trains,
                "utilization_rate": round(eligible_trains / active_trains * 100, 1) if active_trains > 0 else 0
            },
            "maintenance": {
                "open_job_cards": len(open_jobs),
                "trains_need_maintenance": trains_with_open_jobs,
                "maintenance_urgency": "high" if trains_with_open_jobs > 5 else "medium" if trains_with_open_jobs > 2 else "low"
            },
            "branding": {
                "active_contracts": len(active_contracts_list),
                "contracts_need_exposure": contracts_needing_exposure,
                "exposure_gap": sum(max(0, c.exposure_hours_required - c.exposure_hours_fulfilled) for c in active_contracts_list)
            },
            "today_plan": {
                "service_trains": service_trains,
                "standby_trains": standby_trains,
                "total_planned": len(todays_plan_list),
                "approval_status": "approved" if all(p.approved_by for p in todays_plan_list) else "pending"
            },
            "risk_assessment": {
                "high_risk_trains": high_risk_trains,
                "risk_level": "high" if high_risk_trains > 3 else "medium" if high_risk_trains > 1 else "low"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating dashboard overview: {str(e)}"
        )

@router.get("/train-status")
def get_train_status_overview(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get detailed status for all trains"""
    try:
        trains = read_trains(db)
        rule_engine = AdvancedRuleEngine(db)
        
        # Get readiness assessment for all trains
        readiness_assessment = rule_engine._assess_train_readiness(date.today())
        readiness_dict = {t.train_id: t for t in readiness_assessment}
        
        train_status = []
        for train in trains:
            # Get eligibility from readiness assessment
            train_readiness = readiness_dict.get(train.id)
            eligibility_status = train_readiness.status.value if train_readiness else "unknown"
            
            # Get open job cards
            open_jobs = read_open_job_cards(db, train_id=train.id)
            
            # Get active branding contracts
            active_contracts = read_active_contracts(db, train_id=train.id)
            
            # Get today's induction plan
            todays_plan_list = read_todays_plan(db)
            todays_plan = next((p for p in todays_plan_list if p.train_id == train.id), None)
            
            train_status.append({
                "train_id": train.id,
                "train_number": train.train_number,
                "status": train.status,
                "mileage": train.current_mileage,
                "last_maintenance": train.last_maintenance_date.isoformat() if train.last_maintenance_date else None,
                "eligibility": eligibility_status,
                "readiness_score": round(train_readiness.readiness_score, 2) if train_readiness else 0.0,
                "open_job_cards": len(open_jobs),
                "active_branding_contracts": len(active_contracts),
                "today_induction": todays_plan.induction_type if todays_plan else "not_scheduled",
                "today_rank": todays_plan.rank if todays_plan else None
            })
        
        return train_status
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching train status: {str(e)}"
        )

@router.get("/maintenance-alerts")
def get_maintenance_alerts(db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    """Get maintenance alerts and priorities"""
    try:
        open_jobs = read_open_job_cards(db)
        
        alerts = []
        for job in open_jobs:
            train = read_train(db, train_id=job.train_id)
            if train:
                # Simple priority calculation based on job age
                job_age = (datetime.now().date() - job.created_at.date()).days
                priority = "high" if job_age > 7 else "medium" if job_age > 3 else "low"
                
                alerts.append({
                    "job_id": job.id,
                    "work_order_id": job.work_order_id,
                    "train_id": train.id,
                    "train_number": train.train_number,
                    "description": job.description,
                    "priority": priority,
                    "days_open": job_age,
                    "created_date": job.created_at.date().isoformat()
                })
        
        # Sort by priority and age
        priority_order = {"high": 3, "medium": 2, "low": 1}
        alerts.sort(key=lambda x: (priority_order[x["priority"]], x["days_open"]), reverse=True)
        
        return alerts
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching maintenance alerts: {str(e)}"
        )

@router.get("/branding-compliance")
def get_branding_compliance_report(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get branding contract compliance report"""
    try:
        active_contracts = read_active_contracts(db)
        contracts_needing_exposure = read_contracts_need_exposure(db)
        
        compliance_data = []
        total_required = 0
        total_fulfilled = 0
        
        for contract in active_contracts:
            train = read_train(db, train_id=contract.train_id)
            completion_rate = (contract.exposure_hours_fulfilled / contract.exposure_hours_required * 100) if contract.exposure_hours_required > 0 else 0
            days_remaining = (contract.end_date - date.today()).days
            
            compliance_data.append({
                "contract_id": contract.id,
                "advertiser": contract.advertiser_name,
                "train_number": train.train_number if train else "Unknown",
                "required_hours": contract.exposure_hours_required,
                "fulfilled_hours": contract.exposure_hours_fulfilled,
                "completion_rate": round(completion_rate, 1),
                "days_remaining": days_remaining,
                "status": "compliant" if completion_rate >= 80 else "at_risk" if completion_rate >= 50 else "critical"
            })
            
            total_required += contract.exposure_hours_required
            total_fulfilled += contract.exposure_hours_fulfilled
        
        overall_completion = (total_fulfilled / total_required * 100) if total_required > 0 else 0
        
        return {
            "summary": {
                "total_contracts": len(active_contracts),
                "contracts_at_risk": len([c for c in compliance_data if c["status"] == "at_risk"]),
                "contracts_critical": len([c for c in compliance_data if c["status"] == "critical"]),
                "overall_completion": round(overall_completion, 1),
                "total_exposure_gap": total_required - total_fulfilled
            },
            "contracts": compliance_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching branding compliance: {str(e)}"
        )

@router.get("/predictive-analytics")
def get_predictive_analytics(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get predictive analytics and insights"""
    try:
        ml_model = MLModel(db)
        rule_engine = AdvancedRuleEngine(db)
        
        insights = {
            "failure_predictions": {},
            "maintenance_forecast": {},
            "capacity_planning": {},
            "risk_assessment": {}
        }
        
        # Failure predictions
        if ml_model.is_trained:
            predictions = ml_model.predict_all_trains()
            high_risk = [p for p in predictions if p.risk_level == "high"]
            medium_risk = [p for p in predictions if p.risk_level == "medium"]
            
            insights["failure_predictions"] = {
                "high_risk_trains": len(high_risk),
                "medium_risk_trains": len(medium_risk),
                "recommended_maintenance": len(high_risk) + len(medium_risk) // 2,
                "prediction_confidence": "high" if len(predictions) > 5 else "medium"
            }
        
        # Maintenance forecast using rule engine's readiness assessment
        readiness_assessment = rule_engine._assess_train_readiness(date.today())
        maintenance_needed = [t for t in readiness_assessment if t.status == TrainStatus.MAINTENANCE_NEEDED]
        
        insights["maintenance_forecast"] = {
            "maintenance_due_soon": len(maintenance_needed),
            "next_week_maintenance": min(5, len(maintenance_needed)),
            "maintenance_capacity_required": f"{len(maintenance_needed)} trains in next 2 weeks",
            "average_readiness_score": round(sum(t.readiness_score for t in readiness_assessment) / len(readiness_assessment), 2) if readiness_assessment else 0
        }
        
        # Capacity planning using readiness assessment
        eligible_trains = [t for t in readiness_assessment if t.status in [TrainStatus.AVAILABLE, TrainStatus.RESTRICTED]]
        active_contracts = len(read_active_contracts(db))
        
        insights["capacity_planning"] = {
            "available_capacity": len(eligible_trains),
            "branding_demand": active_contracts,
            "capacity_utilization": f"{min(100, (active_contracts / len(eligible_trains) * 100)):.1f}%" if eligible_trains else "0%",
            "recommendation": "Adequate capacity" if len(eligible_trains) > active_contracts + 5 else "Consider adding capacity",
            "high_readiness_trains": len([t for t in eligible_trains if t.readiness_score >= 0.8])
        }
        
        # Overall risk assessment using rule engine's risk factors
        open_jobs = len(read_open_job_cards(db))
        critical_contracts = len([c for c in read_active_contracts(db) 
                                if c.exposure_hours_fulfilled < c.exposure_hours_required * 0.5])
        
        # Calculate average risk factor from readiness assessment
        avg_risk_factor = sum(t.risk_factor for t in readiness_assessment) / len(readiness_assessment) if readiness_assessment else 0.5
        
        risk_score = min(100, (open_jobs * 10) + (critical_contracts * 15) + (len(maintenance_needed) * 5) + (avg_risk_factor * 100))
        
        insights["risk_assessment"] = {
            "risk_score": round(risk_score, 1),
            "risk_level": "high" if risk_score > 70 else "medium" if risk_score > 40 else "low",
            "average_risk_factor": round(avg_risk_factor, 2),
            "major_risks": [
                f"{open_jobs} open maintenance jobs",
                f"{critical_contracts} critical branding contracts",
                f"{len(maintenance_needed)} trains due for maintenance",
                f"Average train risk factor: {avg_risk_factor:.2f}"
            ]
        }
        
        return insights
        
    except Exception as e:
        insights["error"] = f"Analytics generation failed: {str(e)}"
        return insights

@router.get("/train-readiness")
def get_train_readiness_dashboard(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Get detailed train readiness dashboard using the rule engine"""
    try:
        rule_engine = AdvancedRuleEngine(db)
        readiness_assessment = rule_engine._assess_train_readiness(date.today())
        
        # Categorize trains by readiness level
        excellent = [t for t in readiness_assessment if t.readiness_score >= 0.8]
        good = [t for t in readiness_assessment if 0.6 <= t.readiness_score < 0.8]
        fair = [t for t in readiness_assessment if 0.4 <= t.readiness_score < 0.6]
        poor = [t for t in readiness_assessment if t.readiness_score < 0.4]
        
        # Get top constraints
        all_constraints = []
        for train in readiness_assessment:
            all_constraints.extend(train.constraints)
        
        constraint_counts = {}
        for constraint in all_constraints:
            constraint_counts[constraint] = constraint_counts.get(constraint, 0) + 1
        
        return {
            "summary": {
                "total_trains_assessed": len(readiness_assessment),
                "average_readiness_score": round(sum(t.readiness_score for t in readiness_assessment) / len(readiness_assessment), 2),
                "availability_rate": len([t for t in readiness_assessment if t.status in [TrainStatus.AVAILABLE, TrainStatus.RESTRICTED]]) / len(readiness_assessment),
                "readiness_distribution": {
                    "excellent": len(excellent),
                    "good": len(good),
                    "fair": len(fair),
                    "poor": len(poor)
                }
            },
            "top_constraints": dict(sorted(constraint_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
            "trains_need_attention": [
                {
                    "train_id": t.train_id,
                    "train_number": t.train_number,
                    "readiness_score": round(t.readiness_score, 2),
                    "status": t.status.value,
                    "constraints": t.constraints
                }
                for t in readiness_assessment if t.readiness_score < 0.6
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching train readiness data: {str(e)}"
        )