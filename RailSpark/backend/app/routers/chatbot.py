from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from database import get_db
from ai.chatbot import Chatbot, ChatResponse
import schemas

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post("/query")
def process_chatbot_query(
    query: schemas.ChatQuery,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Process chatbot query and return response"""
    chatbot = Chatbot(db)
    
    try:
        response = chatbot.process_message(query.message, query.user_id)
        
        return {
            "message": response.message,
            "data": response.data,
            "type": response.type,
            "timestamp": schemas.datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot error: {str(e)}")

@router.post("/what-if")
def process_what_if_scenario(
    scenario: schemas.WhatIfScenario,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Process what-if scenario analysis"""
    chatbot = Chatbot(db)
    
    try:
        # Construct message for what-if analysis
        message = f"What if {scenario.scenario_type} {scenario.parameters}"
        response = chatbot.process_message(message, scenario.user_id)
        
        return {
            "scenario_type": scenario.scenario_type,
            "parameters": scenario.parameters,
            "analysis": response.message,
            "data": response.data,
            "recommendations": _extract_recommendations(response.message)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"What-if analysis error: {str(e)}")

@router.get("/context/{user_id}")
def get_chatbot_context(user_id: int, db: Session = Depends(get_db)):
    """Get chatbot context for a user"""
    chatbot = Chatbot(db)
    
    return {
        "user_id": user_id,
        "context": chatbot.context.get(user_id, {}),
        "last_interaction": "2024-01-01T00:00:00"  # Would be actual timestamp in production
    }

@router.delete("/context/{user_id}")
def clear_chatbot_context(user_id: int, db: Session = Depends(get_db)):
    """Clear chatbot context for a user"""
    chatbot = Chatbot(db)
    
    if user_id in chatbot.context:
        del chatbot.context[user_id]
    
    return {"message": f"Context cleared for user {user_id}"}

@router.get("/capabilities")
def get_chatbot_capabilities():
    """Get information about chatbot capabilities"""
    return {
        "capabilities": [
            {
                "name": "Schedule Planning",
                "description": "Generate and analyze induction schedules",
                "examples": [
                    "Show me tomorrow's induction plan",
                    "Which trains are available for service?",
                    "Generate optimized schedule for next week"
                ]
            },
            {
                "name": "Train Status",
                "description": "Check train fitness and eligibility",
                "examples": [
                    "Is train KMRL-001 fit for service?",
                    "Show me all trains needing maintenance",
                    "Check fitness certificates for KMRL-002"
                ]
            },
            {
                "name": "What-If Analysis",
                "description": "Simulate different operational scenarios",
                "examples": [
                    "What if I add 2 more trains?",
                    "What if maintenance takes 3 days?",
                    "What if we have 3 new branding contracts?"
                ]
            },
            {
                "name": "Failure Prediction",
                "description": "Predict maintenance needs and failures",
                "examples": [
                    "Predict failure risks for all trains",
                    "Which trains are high risk?",
                    "Show me maintenance recommendations"
                ]
            },
            {
                "name": "Branding Management",
                "description": "Manage advertising contracts and exposure",
                "examples": [
                    "Which branding contracts need attention?",
                    "Show me exposure requirements",
                    "What's our branding capacity?"
                ]
            }
        ],
        "supported_formats": [
            "Natural language queries",
            "What-if scenario analysis", 
            "Structured data requests",
            "Predictive analytics requests"
        ]
    }

def _extract_recommendations(message: str) -> List[str]:
    """Extract recommendations from chatbot response"""
    recommendations = []
    lines = message.split('\n')
    
    for line in lines:
        if 'recommendation:' in line.lower() or '•' in line:
            clean_line = line.replace('•', '').strip()
            if clean_line and len(clean_line) > 10:  # Basic filter for meaningful lines
                recommendations.append(clean_line)
    
    return recommendations if recommendations else ["No specific recommendations generated."]