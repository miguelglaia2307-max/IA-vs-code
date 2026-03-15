from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.database_models import Program
from app.models.schemas import ProgramCreate, ProgramResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=ProgramResponse)
def create_program(program: ProgramCreate, db: Session = Depends(get_db)):
    """Create a new program"""
    db_program = Program(**program.dict())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

@router.get("/", response_model=List[ProgramResponse])
def list_programs(project_id: int = None, db: Session = Depends(get_db)):
    """List all programs, optionally filtered by project"""
    query = db.query(Program)
    if project_id:
        query = query.filter(Program.project_id == project_id)
    return query.all()

@router.get("/{program_id}", response_model=ProgramResponse)
def get_program(program_id: int, db: Session = Depends(get_db)):
    """Get a program by ID"""
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

@router.put("/{program_id}", response_model=ProgramResponse)
def update_program(
    program_id: int,
    program_update: ProgramCreate,
    db: Session = Depends(get_db)
):
    """Update a program"""
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    for key, value in program_update.dict().items():
        setattr(program, key, value)
    
    db.commit()
    db.refresh(program)
    return program

@router.delete("/{program_id}")
def delete_program(program_id: int, db: Session = Depends(get_db)):
    """Delete a program"""
    program = db.query(Program).filter(Program.id == program_id).first()
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    
    db.delete(program)
    db.commit()
    return {"message": "Program deleted"}
