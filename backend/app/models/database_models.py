from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Signature(Base):
    __tablename__ = "signatures"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    name = Column(String)
    description = Column(String)
    input_fields = Column(JSON)  # List of input field definitions
    output_fields = Column(JSON)  # List of output field definitions
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    signature_id = Column(Integer, index=True)
    name = Column(String)
    examples = Column(JSON)  # List of input-output examples
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    signature_id = Column(Integer, index=True)
    name = Column(String)
    metric_type = Column(String)  # 'exact_match', 'similarity', 'custom', etc.
    config = Column(JSON)  # Configuration for the metric
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    signature_id = Column(Integer, index=True)
    name = Column(String)
    description = Column(String)
    code = Column(String)  # Python code or prompt template
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OptimizationRun(Base):
    __tablename__ = "optimization_runs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, index=True)
    signature_id = Column(Integer, index=True)
    program_id = Column(Integer, index=True)
    metric_id = Column(Integer, index=True)
    dataset_id = Column(Integer, index=True)
    status = Column(String, default="pending")  # pending, running, completed, failed
    initial_prompt = Column(String)
    best_prompt = Column(String)
    best_score = Column(Float)
    iterations = Column(Integer, default=0)
    results = Column(JSON)  # Results from each iteration
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class PromptVariation(Base):
    __tablename__ = "prompt_variations"

    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(Integer, index=True)
    prompt = Column(String)
    score = Column(Float)
    iteration = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
