"""
Celery Async Tasks Configuration

Handles background jobs like optimization runs, email notifications, etc.
"""

import os
from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

# Initialize Celery
celery_app = Celery(
    "prompt_optimization",
    broker=settings.celery_broker_url or "redis://localhost:6379/1",
    backend=settings.celery_result_backend or "redis://localhost:6379/2"
)

# Load configuration from settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_acks_late=True,
    task_track_started=True,
    task_time_limit=settings.timeout_seconds,
    task_soft_time_limit=settings.timeout_seconds - 10,
)

# Scheduled tasks
celery_app.conf.beat_schedule = {
    "cleanup-expired-optimizations": {
        "task": "app.services.async_tasks.cleanup_expired_optimizations",
        "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    "generate-optimization-reports": {
        "task": "app.services.async_tasks.generate_optimization_reports",
        "schedule": crontab(hour=1, minute=0),  # Daily at 1 AM
    },
}

# Task definitions
@celery_app.task(bind=True, name="run_optimization_async")
def run_optimization_async(self, optimization_run_id: int):
    """
    Run optimization asynchronously
    """
    from app.core.database import SessionLocal
    from app.models.database_models import OptimizationRun
    from app.services.optimizer import PromptOptimizer
    from app.services.ai_agents import AI_ORCHESTRATOR
    
    try:
        db = SessionLocal()
        
        # Get optimization run
        opt_run = db.query(OptimizationRun).filter(
            OptimizationRun.id == optimization_run_id
        ).first()
        
        if not opt_run:
            self.update_state(state="FAILED")
            return {"error": "Optimization run not found"}
        
        # Run optimization
        optimizer = PromptOptimizer(api_key=settings.openai_api_key)
        results = []
        
        for iteration in range(settings.max_iterations):
            # Update progress
            progress = int((iteration + 1) / settings.max_iterations * 100)
            self.update_state(
                state="PROGRESS",
                meta={"current": iteration + 1, "total": settings.max_iterations, "progress": progress}
            )
            
            # Generate variations
            variations = optimizer.generate_variations(
                initial_prompt=opt_run.initial_prompt,
                num_variations=settings.variations_per_iteration
            )
            
            # Evaluate variations and track results
            for var in variations:
                # Evaluation logic here
                results.append({"prompt": var, "score": 0.5})
            
            # Use AI Orchestrator for adaptive optimization
            if AI_ORCHESTRATOR and iteration % 2 == 0:
                strategy = AI_ORCHESTRATOR.orchestrate_optimization(
                    initial_prompt=opt_run.initial_prompt,
                    task_description=opt_run.signature.task_description,
                    current_iteration=iteration,
                    best_score=max([r.get("score", 0) for r in results], default=0),
                    all_results=results
                )
        
        db.close()
        return {
            "status": "completed",
            "optimization_run_id": optimization_run_id,
            "results": results
        }
    
    except Exception as e:
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise

@celery_app.task(bind=True, name="generate_ai_insights")
def generate_ai_insights(self, optimization_run_id: int):
    """
    Generate AI-powered insights for completed optimization
    """
    from app.services.ai_agents import AI_ORCHESTRATOR
    
    try:
        if not AI_ORCHESTRATOR:
            return {"error": "AI orchestrator not available"}
        
        # Generate insights using AI agents
        insights = AI_ORCHESTRATOR.result_analyzer.execute(
            optimization_results=[],  # Fetch from DB
            dataset_size=0,
            evaluation_metric="multi-metric"
        )
        
        return {"insights": insights, "optimization_run_id": optimization_run_id}
    
    except Exception as e:
        self.update_state(state="FAILURE", meta={"error": str(e)})
        raise

@celery_app.task(name="cleanup_expired_optimizations")
def cleanup_expired_optimizations():
    """
    Clean up old optimization runs (older than 30 days)
    """
    from datetime import datetime, timedelta
    from app.core.database import SessionLocal
    from app.models.database_models import OptimizationRun
    
    try:
        db = SessionLocal()
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        deleted_count = db.query(OptimizationRun).filter(
            OptimizationRun.created_at < cutoff_date
        ).delete()
        
        db.commit()
        db.close()
        
        return {"deleted_count": deleted_count}
    
    except Exception as e:
        return {"error": str(e)}

@celery_app.task(name="generate_optimization_reports")
def generate_optimization_reports():
    """
    Generate daily optimization reports
    """
    from datetime import datetime, timedelta
    from app.core.database import SessionLocal
    from app.models.database_models import OptimizationRun, Project
    
    try:
        db = SessionLocal()
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        # Get optimizations from last 24 hours
        recent_optimizations = db.query(OptimizationRun).filter(
            OptimizationRun.created_at >= yesterday
        ).all()
        
        # Group by project and generate statistics
        reports = {}
        for opt in recent_optimizations:
            project_id = opt.project_id
            if project_id not in reports:
                reports[project_id] = {
                    "total_optimizations": 0,
                    "avg_improvement": 0,
                    "status_counts": {}
                }
            reports[project_id]["total_optimizations"] += 1
        
        db.close()
        
        return {"reports_generated": len(reports), "timestamp": datetime.utcnow().isoformat()}
    
    except Exception as e:
        return {"error": str(e)}

# Health check task
@celery_app.task(name="health_check")
def health_check():
    """
    Simple health check task for monitoring
    """
    return {"status": "healthy", "timestamp": os.urandom(8).hex()}
