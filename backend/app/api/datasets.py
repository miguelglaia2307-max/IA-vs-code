from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.database_models import Dataset
from app.models.schemas import DatasetCreate, DatasetResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=DatasetResponse)
def create_dataset(dataset: DatasetCreate, db: Session = Depends(get_db)):
    """Create a new dataset"""
    db_dataset = Dataset(**dataset.dict())
    db.add(db_dataset)
    db.commit()
    db.refresh(db_dataset)
    return db_dataset

@router.get("/", response_model=List[DatasetResponse])
def list_datasets(project_id: int = None, db: Session = Depends(get_db)):
    """List all datasets, optionally filtered by project"""
    query = db.query(Dataset)
    if project_id:
        query = query.filter(Dataset.project_id == project_id)
    return query.all()

@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Get a dataset by ID"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

@router.put("/{dataset_id}", response_model=DatasetResponse)
def update_dataset(
    dataset_id: int,
    dataset_update: DatasetCreate,
    db: Session = Depends(get_db)
):
    """Update a dataset"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    for key, value in dataset_update.dict().items():
        setattr(dataset, key, value)
    
    db.commit()
    db.refresh(dataset)
    return dataset

@router.delete("/{dataset_id}")
def delete_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Delete a dataset"""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    db.delete(dataset)
    db.commit()
    return {"message": "Dataset deleted"}
