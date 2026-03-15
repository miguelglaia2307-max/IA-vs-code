# System Architecture

## Overview

The Prompt Optimization Platform consists of three main layers:

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Pages & Components                                     │ │
│  │ - Landing Page (with Three.js WebGL effects)          │ │
│  │ - Dashboard (Project management)                       │ │
│  │ - Optimization Runner                                  │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ API Client (axios/fetch)                              │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↓
                    HTTP REST API
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ API Routes                                             │ │
│  │ - /api/projects/                                       │ │
│  │ - /api/optimization/                                   │ │
│  │ - /api/signatures/                                     │ │
│  │ - /api/datasets/                                       │ │
│  │ - /api/metrics/                                        │ │
│  │ - /api/programs/                                       │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Service Layer                                          │ │
│  │ - PromptOptimizer (Core optimization logic)           │ │
│  │ - LLM Integration (OpenAI)                             │ │
│  │ - Metrics Evaluation                                   │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Data Access Layer                                      │ │
│  │ - SQLAlchemy ORM                                       │ │
│  │ - Database Models                                      │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           ↓
                      SQL Queries
                           ↓
┌─────────────────────────────────────────────────────────────┐
│              Database (SQLite/PostgreSQL)                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Tables:                                                │ │
│  │ - projects          - metrics                          │ │
│  │ - signatures        - programs                         │ │
│  │ - datasets          - optimization_runs                │ │
│  │ - prompt_variations                                    │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Frontend Architecture

### Component Hierarchy

```
App (Layout)
├── LandingPage
│   ├── Canvas3D (Three.js WebGL rendering)
│   ├── HeroSection
│   └── Features
└── Dashboard (To be implemented)
    ├── ProjectsList
    ├── OptimizationRunner
    └── ProgressMonitor
```

### Data Flow

```
User Interaction
        ↓
React Component
        ↓
API Client (axios)
        ↓
Backend API (HTTP)
        ↓
Component State Update
        ↓
UI Re-render
```

## Backend Architecture

### Optimization Loop Flow

```
┌─────────────────────┐
│  Initial Prompt     │
│  (User Provided)    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Generate           │
│  Variations         │
│  (LLM-based)        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Evaluate Each      │
│  Variation on       │
│  Dataset Examples   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Calculate Scores   │
│  Using Metrics      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Select Best        │
│  Performer          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Converged?         │ ──No──┐
│  (Iterations done)  |       │
└──────────┬──────────┘       │
      Yes │                   │
          ↓                   │
┌─────────────────────┐       │
│  Best Prompt Found  │◄──Repeat
│  (Save Results)     │
└─────────────────────┘
```

### Request Handling Flow

```
HTTP Request
        ↓
FastAPI Router
        ↓
Dependency Injection (get_db)
        ↓
Handler Function
        ↓
Service Layer (Business Logic)
        ↓
ORM Query
        ↓
Database
        ↓
Response Serialization (Pydantic)
        ↓
HTTP Response
```

## Data Models Relationships

```
Project
├── has many Signatures
├── has many Datasets
├── has many Metrics
├── has many Programs
└── has many OptimizationRuns

Signature
├── has many Datasets
├── has many Metrics
├── has many Programs
└── has many OptimizationRuns

OptimizationRun
├── references Signature
├── references Program
├── references Metric
├── references Dataset
└── has many PromptVariations

PromptVariation
└── references OptimizationRun
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (React meta-framework)
- **Language**: TypeScript (type-safe JavaScript)
- **Styling**: Tailwind CSS (utility-first CSS)
- **3D Graphics**: Three.js (WebGL library)
- **HTTP Client**: axios (HTTP requests)
- **State Management**: React Hooks (built-in)

### Backend
- **Framework**: FastAPI (modern Python web framework)
- **Language**: Python 3.11+
- **Database ORM**: SQLAlchemy 2.0
- **Validation**: Pydantic (data validation)
- **Database**: SQLite (default) / PostgreSQL
- **Async Support**: asyncio with async/await
- **LLM Integration**: OpenAI API

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Version Control**: Git
- **CI/CD**: GitHub Actions (to be configured)

## Deployment Architecture

### Development
```
Local Machine
├── Frontend (port 3000)
└── Backend (port 8000)
```

### Docker
```
Docker Host
├── Frontend Container (Node.js)
└── Backend Container (Python)
```

## Security Considerations

1. **API Authentication**: (To be implemented)
   - JWT tokens for user authentication
   - API key validation

2. **Data Validation**: 
   - Pydantic models for input validation
   - SQLAlchemy prevents SQL injection

3. **CORS**: Configured in FastAPI

4. **Environment Secrets**:
   - Use .env files (excluded from git)
   - Store sensitive data (API keys) securely

## Scalability Considerations

1. **Database**:
   - Switch from SQLite to PostgreSQL for concurrent access
   - Add database indexing for frequently queried fields
   - Implement connection pooling

2. **API**:
   - Use multiple worker processes (Gunicorn)
   - Implement caching (Redis)
   - Add rate limiting

3. **Frontend**:
   - Static site generation (SSG) for pages
   - Implement service workers for offline support
   - Use CDN for asset delivery

## Monitoring & Logging

(To be implemented)
- Application logging
- Performance monitoring
- Error tracking
- Health checks
