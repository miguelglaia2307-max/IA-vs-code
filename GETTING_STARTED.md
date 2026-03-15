# Getting Started with Development

## Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- Git

## Quick Start (5 minutes)

### 1. Start Backend

```bash
cd backend
pip install -r requirements.txt
python seed.py       # Populate database with test data
python run.py        # Start backend server
```

Backend will be available at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

### 2. Start Frontend (new terminal)

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### 3. Access the Application

- **Landing Page**: http://localhost:3000
- **Dashboard**: http://localhost:3000/dashboard
- **API Documentation**: http://localhost:8000/docs

## Project Features

### ✅ Fully Implemented

1. **Landing Page** - Beautiful WebGL-powered interface with Three.js animations
2. **API Routes** - Complete CRUD for Projects, Signatures, Datasets, Metrics, Programs
3. **Dashboard** - Manage projects and view optimization runs
4. **Optimization Loop** - Automated prompt optimization with multiple evaluation metrics
5. **Frontend Components** - Dashboard, Project Details, Optimization Monitor

### 🔄 In Progress / Next Steps

1. Authentication (JWT tokens)
2. WebSocket for real-time updates
3. Admin panel for configuration
4. Export optimized prompts
5. Advanced metrics and scoring

## Test the Optimization

### Using the Web Interface

1. Open http://localhost:3000/dashboard
2. You should see a test project "Customer Service Optimization" (created by seed.py)
3. Click "Open" to view the project
4. Click "▶ Iniciar Nova Otimização" to start optimization
5. Enter a prompt like: `You are a helpful customer service agent`
6. Click the optimization link to watch progress in real-time

### Using the API Directly

```bash
# Get projects
curl http://localhost:8000/api/projects/

# Start optimization
curl -X POST http://localhost:8000/api/optimization/run \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "signature_id": 1,
    "program_id": 1,
    "metric_id": 1,
    "dataset_id": 1,
    "initial_prompt": "You are a helpful customer service agent"
  }'

# Get optimization run details
curl http://localhost:8000/api/optimization/1

# Get prompt variations
curl http://localhost:8000/api/optimization/1/variations
```

## Architecture

```
Frontend (Next.js + React + TypeScript)
         ↓
    API HTTP (REST)
         ↓
Backend (FastAPI + Python)
         ↓
    SQLAlchemy ORM
         ↓
Database (SQLite by default)
```

## Key Files

### Backend
- `app/main.py` - FastAPI application
- `app/api/` - Route handlers (projects, signatures, datasets, metrics, programs, optimization)
- `app/services/optimizer.py` - Prompt optimization logic
- `app/models/database_models.py` - Database models

### Frontend
- `src/app/page.tsx` - Landing page
- `src/app/dashboard/` - Dashboard pages
- `src/components/` - React components
- `src/services/api.ts` - API client
- `src/types/` - TypeScript interfaces

## Environment Variables

### Backend (.env)
```
DATABASE_URL=sqlite:///./prompt_optimization.db
OPENAI_API_KEY=sk-your-api-key  # Optional - fallback to simple variations if not set
DEBUG=true
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Common Commands

### Backend
```bash
cd backend

# Install requirements
pip install -r requirements.txt

# Seed database
python seed.py

# Run server
python run.py

# Run tests (placeholder)
pytest
```

### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Run tests (placeholder)
npm test
```

## Troubleshooting

### Backend won't start
```bash
# Check if database exists and reset it
rm prompt_optimization.db
python seed.py
python run.py
```

### Frontend won't connect to backend
- Check NEXT_PUBLIC_API_URL in frontend .env.local
- Make sure backend is running on http://localhost:8000

### CORS Issues
- Backend already has CORS configured for all origins (*) in app/main.py
- If you still have issues, check the error in browser console

### Port already in use
```bash
# Find process using port 8000/3000 and kill it
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

## Next Development Steps

1. **Add Authentication**
   - JWT tokens in utils/security.py
   - Login/Register pages
   - Protected routes

2. **Improve Optimizer**
   - Add embedding-based similarity
   - Support multiple LLM providers
   - Implement more evaluation metrics

3. **Real-time Updates**
   - WebSocket support for live optimization progress
   - Real-time dashboard updates

4. **Data Persistence**
   - Export optimization results
   - Save favorite prompts
   - Track optimization history

5. **Advanced Features**
   - Batch optimization
   - Prompt templates library
   - A/B testing
   - Analytics dashboard

## Useful Links

- [Next.js Docs](https://nextjs.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Three.js Docs](https://threejs.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [OpenAI API Docs](https://platform.openai.com/docs)

## Support

For issues or questions:
1. Check the logs in terminal
2. Visit http://localhost:8000/docs for API documentation
3. Check console in browser DevTools (F12)
4. Review error messages carefully - they usually point to the solution
