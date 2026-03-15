import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import projects, optimization, signatures, datasets, metrics, programs, auth, monitoring
from app.core.database import engine, Base
from app.middleware.error_handler import ErrorHandlingMiddleware, add_error_handlers
from app.services.logger import logger

# Create tables
Base.metadata.create_all(bind=engine)

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Prompt Optimization API...")
    yield
    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title="Prompt Optimization API",
    description="API for automated prompt optimization",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
)

# Error handling middleware
app.add_middleware(ErrorHandlingMiddleware)

# Add global error handlers
add_error_handlers(app)

# CORS middleware — restrict origins in production
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if DEBUG or not any(allowed_origins):
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(signatures.router, prefix="/api/signatures", tags=["signatures"])
app.include_router(datasets.router, prefix="/api/datasets", tags=["datasets"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])
app.include_router(programs.router, prefix="/api/programs", tags=["programs"])
app.include_router(optimization.router, prefix="/api/optimization", tags=["optimization"])
app.include_router(monitoring.router)

@app.get("/")
async def root():
    return {
        "message": "Prompt Optimization Platform API",
        "version": "0.1.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
