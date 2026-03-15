from pydantic import BaseModel, field_validator
from typing import List, Dict, Any, Optional
from datetime import datetime

# Project Schemas
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Signature Schemas
class SignatureCreate(BaseModel):
    project_id: int
    name: str
    description: Optional[str] = None
    input_fields: List[Dict[str, Any]]
    output_fields: List[Dict[str, Any]]

class SignatureResponse(BaseModel):
    id: int
    project_id: int
    name: str
    description: Optional[str]
    input_fields: List[Dict[str, Any]]
    output_fields: List[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True

# Dataset Schemas
class DatasetCreate(BaseModel):
    project_id: int
    signature_id: int
    name: str
    examples: List[Dict[str, Any]]

class DatasetResponse(BaseModel):
    id: int
    project_id: int
    signature_id: int
    name: str
    examples: List[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True

# Metric Schemas
class MetricCreate(BaseModel):
    project_id: int
    signature_id: int
    name: str
    metric_type: str
    config: Optional[Dict[str, Any]] = None

class MetricResponse(BaseModel):
    id: int
    project_id: int
    signature_id: int
    name: str
    metric_type: str
    config: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True

# Program Schemas
class ProgramCreate(BaseModel):
    project_id: int
    signature_id: int
    name: str
    description: Optional[str] = None
    code: str

class ProgramResponse(BaseModel):
    id: int
    project_id: int
    signature_id: int
    name: str
    description: Optional[str]
    code: str
    created_at: datetime

    class Config:
        from_attributes = True

# Optimization Run Schemas
class OptimizationRunCreate(BaseModel):
    project_id: int
    signature_id: int
    program_id: int
    metric_id: int
    dataset_id: int
    initial_prompt: str

class OptimizationRunResponse(BaseModel):
    id: int
    project_id: int
    signature_id: int
    program_id: int
    metric_id: int
    dataset_id: int
    status: str
    initial_prompt: str
    best_prompt: Optional[str]
    best_score: Optional[float]
    iterations: int
    results: Optional[List[Dict[str, Any]]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Authentication Schemas
class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    
    @field_validator('password')
    @classmethod
    def validate_password_length(cls, v):
        if len(v.encode('utf-8')) > 72:
            raise ValueError('Password must be at most 72 bytes (usually ~ 72 characters)')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    user_id: Optional[int] = None

# Error Reporting Schemas
class ErrorReport(BaseModel):
    errorType: str
    message: str
    context: Optional[Dict[str, Any]] = None
    traceback: Optional[str] = None
    timestamp: str
    url: Optional[str] = None
    userAgent: Optional[str] = None

class ErrorReportResponse(BaseModel):
    status: str
    message: str
