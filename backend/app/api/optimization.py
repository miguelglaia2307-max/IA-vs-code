from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.database_models import (
    OptimizationRun, Signature, Program, Metric, Dataset, PromptVariation
)
from app.models.schemas import OptimizationRunCreate, OptimizationRunResponse
from typing import List
from app.services.optimizer import run_optimization_async

router = APIRouter()

@router.post("/run", response_model=OptimizationRunResponse)
def create_optimization_run(
    run: OptimizationRunCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create and start a new optimization run"""
    
    # Verify all referenced entities exist
    signature = db.query(Signature).filter(Signature.id == run.signature_id).first()
    if not signature:
        raise HTTPException(status_code=404, detail="Signature not found")
    
    program = db.query(Program).filter(Program.id == run.program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    metric = db.query(Metric).filter(Metric.id == run.metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    dataset = db.query(Dataset).filter(Dataset.id == run.dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Create the optimization run
    db_run = OptimizationRun(**run.dict(), status="pending")
    db.add(db_run)
    db.commit()
    db.refresh(db_run)
    
    # Start optimization in background
    background_tasks.add_task(
        run_optimization_async,
        run_id=db_run.id,
        program_id=run.program_id,
        metric_id=run.metric_id,
        dataset_id=run.dataset_id
    )
    
    return db_run

@router.get("/runs", response_model=List[OptimizationRunResponse])
def list_optimization_runs(
    project_id: int = None,
    db: Session = Depends(get_db)
):
    """List all optimization runs"""
    query = db.query(OptimizationRun)
    if project_id:
        query = query.filter(OptimizationRun.project_id == project_id)
    return query.all()

@router.get("/{run_id}", response_model=OptimizationRunResponse)
def get_optimization_run(run_id: int, db: Session = Depends(get_db)):
    """Get a specific optimization run"""
    run = db.query(OptimizationRun).filter(OptimizationRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Optimization run not found")
    return run

@router.get("/{run_id}/variations")
def get_run_variations(run_id: int, db: Session = Depends(get_db)):
    """Get all prompt variations from a run"""
    variations = db.query(PromptVariation).filter(
        PromptVariation.run_id == run_id
    ).order_by(PromptVariation.iteration).all()
    return variations

@router.post("/{run_id}/stop")
def stop_optimization_run(run_id: int, db: Session = Depends(get_db)):
    """Stop an ongoing optimization run"""
    run = db.query(OptimizationRun).filter(OptimizationRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Optimization run not found")
    
    if run.status == "running":
        run.status = "stopped"
        db.commit()
        return {"message": "Optimization run stopped"}
    
    return {"message": "Run is not currently running"}
