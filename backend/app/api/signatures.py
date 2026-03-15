from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.database_models import Signature
from app.models.schemas import SignatureCreate, SignatureResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=SignatureResponse)
def create_signature(signature: SignatureCreate, db: Session = Depends(get_db)):
    """Create a new signature"""
    db_signature = Signature(**signature.dict())
    db.add(db_signature)
    db.commit()
    db.refresh(db_signature)
    return db_signature

@router.get("/", response_model=List[SignatureResponse])
def list_signatures(project_id: int = None, db: Session = Depends(get_db)):
    """List all signatures, optionally filtered by project"""
    query = db.query(Signature)
    if project_id:
        query = query.filter(Signature.project_id == project_id)
    return query.all()

@router.get("/{signature_id}", response_model=SignatureResponse)
def get_signature(signature_id: int, db: Session = Depends(get_db)):
    """Get a signature by ID"""
    signature = db.query(Signature).filter(Signature.id == signature_id).first()
    if not signature:
        raise HTTPException(status_code=404, detail="Signature not found")
    return signature

@router.put("/{signature_id}", response_model=SignatureResponse)
def update_signature(
    signature_id: int,
    signature_update: SignatureCreate,
    db: Session = Depends(get_db)
):
    """Update a signature"""
    signature = db.query(Signature).filter(Signature.id == signature_id).first()
    if not signature:
        raise HTTPException(status_code=404, detail="Signature not found")
    
    for key, value in signature_update.dict().items():
        setattr(signature, key, value)
    
    db.commit()
    db.refresh(signature)
    return signature

@router.delete("/{signature_id}")
def delete_signature(signature_id: int, db: Session = Depends(get_db)):
    """Delete a signature"""
    signature = db.query(Signature).filter(Signature.id == signature_id).first()
    if not signature:
        raise HTTPException(status_code=404, detail="Signature not found")
    
    db.delete(signature)
    db.commit()
    return {"message": "Signature deleted"}
