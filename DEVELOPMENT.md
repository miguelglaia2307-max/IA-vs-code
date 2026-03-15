# Development Guide

## Architecture Overview

### Frontend Architecture

The frontend is built with Next.js 14 using TypeScript and features:
- **App Router**: Modern file-based routing system
- **React Components**: Reusable UI components
- **Three.js**: WebGL rendering for 3D effects
- **Tailwind CSS**: Utility-first styling

### Backend Architecture

The backend follows a layered architecture:
- **API Layer** (`app/api/`): REST endpoints
- **Service Layer** (`app/services/`): Business logic
- **Data Layer** (`app/models/`): Data models and database operations
- **Core Layer** (`app/core/`): Configuration and utilities

## Database Schema

The system uses SQLAlchemy ORM with the following main tables:

### Projects
- Central entity for organizing optimization tasks

### Signatures
- Define the task contract (inputs/outputs)

### Datasets
- Store input/output examples for training

### Metrics
- Define how to measure success

### Programs
- Contain the optimization logic or prompt templates

### OptimizationRuns
- Track individual optimization executions

### PromptVariations
- Store the variations generated during optimization

## Adding New Features

### Adding a New API Endpoint

1. Create a new file in `backend/app/api/` (e.g., `new_feature.py`)
2. Define your router using FastAPI:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()

@router.get("/endpoint")
def get_data(db: Session = Depends(get_db)):
    return {"data": "value"}
```

3. Include the router in `app/main.py`:
```python
from app.api import new_feature
app.include_router(new_feature.router, prefix="/api/new", tags=["new"])
```

### Adding a New Database Model

1. Create the model in `backend/app/models/database_models.py`:
```python
from sqlalchemy import Column, String, Integer
from app.core.database import Base

class NewModel(Base):
    __tablename__ = "new_models"
    id = Column(Integer, primary_key=True)
    name = Column(String)
```

2. Create a Pydantic schema in `backend/app/models/schemas.py`:
```python
class NewModelCreate(BaseModel):
    name: str

class NewModelResponse(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True
```

### Adding a New Frontend Component

1. Create component file in `frontend/src/components/`:
```typescript
'use client'  // Add for interactive components
import React from 'react'

export default function NewComponent() {
  return (
    <div className="p-4 bg-dark-secondary rounded-lg">
      {/* Component content */}
    </div>
  )
}
```

2. Import and use in your page or other components

## Code Style

### Python
- Follow PEP 8 guidelines
- Use type hints for functions
- Format with Black (configured in settings)
- Use 100 character line length

### TypeScript/JavaScript
- Use TypeScript for type safety
- Follow ESLint configuration
- Use functional components with hooks
- Format with Prettier

## Testing

### Frontend Testing
(Placeholder - testing setup to be added)

```bash
cd frontend
npm test
```

### Backend Testing
(Placeholder - testing setup to be added)

```bash
cd backend
pytest
```

## Performance Tips

### Frontend
- Use Next.js image optimization: `<Image>` component
- Implement code splitting for large components
- Profile with Chrome DevTools
- Use React DevTools for component profiling

### Backend
- Use database indexing for frequently queried fields
- Implement caching for expensive operations
- Use async/await for I/O operations
- Monitor API response times

## Deployment

### Build for Production

Frontend:
```bash
cd frontend
npm run build
npm start
```

Backend:
```bash
cd backend
pip install -r requirements.txt
gunicorn app.main:app --bind 0.0.0.0:8000
```

### Environment Variables

Create `.env` files in both directories with production values:

Frontend `.env.production`:
```
NEXT_PUBLIC_API_URL=https://api.example.com
```

Backend `.env`:
```
DATABASE_URL=postgresql://user:password@host/dbname
OPENAI_API_KEY=sk-...
DEBUG=false
```

## Debugging

### Frontend Debugging
- Use React DevTools browser extension
- Use Chrome DevTools for performance profiling
- Check network requests in DevTools Network tab
- Use console logging and breakpoints

### Backend Debugging
- Use Python debugger: `pdb.set_trace()`
- Check logs for error messages
- Use VS Code Python debugger
- Monitor database queries

## Common Issues

### Port Already in Use
- Kill process using the port: Windows: `netstat -ano | findstr :8000` then `taskkill /PID <PID> /F`
- Or change the port in configuration

### Module Not Found
- Ensure virtual environment is activated
- Reinstall dependencies
- Check PYTHONPATH

### Build Failures
- Clear build artifacts: `.next` and `__pycache__`
- Ensure all dependencies are installed
- Check for syntax errors

## Version Pinning

Keep track of critical versions:
- Python 3.11+
- Node.js 18+
- Next.js 14+
- FastAPI 0.104+
- SQLAlchemy 2.0+

## Commits and PRs

### Commit Messages
Use conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting
- `refactor:` for code organization
- `test:` for tests

Example:
```
feat: add prompt variation export

- Export variations to CSV format
- Add timestamp to exports
- Closes #123
```

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Three.js Documentation](https://threejs.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
