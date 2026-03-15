"""
Monitoring and Error Recovery endpoints
"""
from fastapi import APIRouter, Depends
from typing import List, Optional
from app.services.logger import logger
from app.services.error_recovery import error_agent
from app.models.database_models import User
from app.models.schemas import ErrorReport, ErrorReportResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/api/monitoring", tags=["monitoring"])

@router.post("/errors/report", response_model=ErrorReportResponse)
async def report_error(error_report: ErrorReport):
    """Report an error from frontend or backend"""
    logger.log_error(
        error_type=error_report.errorType,
        message=error_report.message,
        context={
            "source": "frontend",
            "url": error_report.url,
            "userAgent": error_report.userAgent,
            **(error_report.context or {})
        },
        traceback_str=error_report.traceback
    )
    
    return {
        "status": "success",
        "message": "Error logged successfully"
    }

@router.get("/errors/recent")
def get_recent_errors(limit: int = 50, current_user: User = Depends(get_current_user)):
    """Get recent errors (admin only)"""
    # In production, check if user is admin
    errors = logger.get_recent_errors(limit=limit)
    return {
        "status": "success",
        "count": len(errors),
        "errors": errors
    }

@router.post("/errors/analyze")
def analyze_error(
    error_type: str,
    message: str,
    context: dict = None,
    traceback_str: str = None,
    current_user: User = Depends(get_current_user)
):
    """Analyze an error using AI"""
    # Log the analysis request
    logger.log_info("Analysis requested", {
        "user_id": current_user.id,
        "error_type": error_type
    })
    
    analysis = error_agent.analyze_error(error_type, message, context, traceback_str)
    return analysis

@router.post("/errors/fix-suggestion")
def get_fix_suggestion(
    error_type: str,
    message: str,
    previous_attempts: List[str] = None,
    current_user: User = Depends(get_current_user)
):
    """Get AI suggested fix for an error"""
    logger.log_info("Fix suggestion requested", {
        "user_id": current_user.id,
        "error_type": error_type
    })
    
    fix = error_agent.suggest_fix(error_type, message, previous_attempts)
    return fix

@router.get("/health/ai-agent")
def ai_agent_health():
    """Check if AI error recovery agent is available"""
    is_healthy = error_agent.health_check()
    return {
        "status": "healthy" if is_healthy else "degraded",
        "ai_available": is_healthy,
        "service": "error_recovery_agent"
    }

@router.get("/dashboard")
def monitoring_dashboard(current_user: User = Depends(get_current_user)):
    """Get monitoring dashboard data (requires auth)"""
    recent_errors = logger.get_recent_errors(limit=20)
    
    # Count errors by type
    error_counts = {}
    for error in recent_errors:
        error_type = error.get("type", "unknown")
        error_counts[error_type] = error_counts.get(error_type, 0) + 1
    
    ai_health = error_agent.health_check()
    
    return {
        "status": "success",
        "total_recent_errors": len(recent_errors),
        "error_counts": error_counts,
        "ai_agent_healthy": ai_health,
        "recent_errors": recent_errors[-10:],  # Last 10
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email
        }
    }

@router.get("/dashboard-public")
def monitoring_dashboard_public():
    """Get monitoring dashboard data (public - no auth required)"""
    recent_errors = logger.get_recent_errors(limit=20)
    
    # Count errors by type
    error_counts = {}
    for error in recent_errors:
        error_type = error.get("type", "unknown")
        error_counts[error_type] = error_counts.get(error_type, 0) + 1
    
    ai_health = error_agent.health_check()
    
    return {
        "status": "success",
        "total_recent_errors": len(recent_errors),
        "error_counts": error_counts,
        "ai_agent_healthy": ai_health,
        "recent_errors": recent_errors[-10:],  # Last 10
        "user": {
            "id": 0,
            "username": "guest",
            "email": "guest@localhost"
        }
    }
