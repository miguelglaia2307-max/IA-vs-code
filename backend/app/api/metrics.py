from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.database_models import Metric
from app.models.schemas import MetricCreate, MetricResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=MetricResponse)
def create_metric(metric: MetricCreate, db: Session = Depends(get_db)):
    """Create a new metric"""
    db_metric = Metric(**metric.dict())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

@router.get("/", response_model=List[MetricResponse])
def list_metrics(project_id: int = None, db: Session = Depends(get_db)):
    """List all metrics, optionally filtered by project"""
    query = db.query(Metric)
    if project_id:
        query = query.filter(Metric.project_id == project_id)
    return query.all()

@router.get("/{metric_id}", response_model=MetricResponse)
def get_metric(metric_id: int, db: Session = Depends(get_db)):
    """Get a metric by ID"""
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric

@router.put("/{metric_id}", response_model=MetricResponse)
def update_metric(
    metric_id: int,
    metric_update: MetricCreate,
    db: Session = Depends(get_db)
):
    """Update a metric"""
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    for key, value in metric_update.dict().items():
        setattr(metric, key, value)
    
    db.commit()
    db.refresh(metric)
    return metric

@router.delete("/{metric_id}")
def delete_metric(metric_id: int, db: Session = Depends(get_db)):
    """Delete a metric"""
    metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    db.delete(metric)
    db.commit()
    return {"message": "Metric deleted"}
