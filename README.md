# Prompt Optimization Platform

A full-stack platform for automatically optimizing your prompts using an intelligent optimization loop. The system implements a sophisticated prompt improvement engine that generates variations, evaluates them, and converges on the best solution automatically.

⭐ **[👉 Get Started in 5 Minutes](./GETTING_STARTED.md)**

## 🎯 How It Works

The platform implements a four-step optimization loop:

1. **Signature** - Define the task contract (inputs/outputs)
2. **Program** - Execute the optimization logic  
3. **Metric** - Measure success with custom evaluation metrics
4. **Dataset** - Provide input/output examples for training

The optimizer automatically:
- Generates prompt variations using LLM
- Evaluates each variation against your dataset
- Calculates scores using your metrics
- Keeps the best performer
- Repeats until convergence

## ✨ Key Features

### 🎨 Frontend
- Modern landing page with WebGL effects (Three.js)
- Complete dashboard for managing projects
- Real-time monitoring of optimization progress
- Responsive design for all devices
- Beautiful dark theme with cyan accents

### 🚀 Backend
- RESTful API with complete CRUD operations
- Prompt optimization engine with multiple evaluation metrics
- LLM integration with OpenAI (fallback support)
- SQLAlchemy database with SQLite/PostgreSQL support
- Async background tasks for long-running optimizations
- Comprehensive Swagger API documentation

## 🏗️ Project Structure

```
.
├── frontend/                    # Next.js React frontend
│   ├── src/app/                # Pages and routing
│   ├── src/components/         # React components
│   ├── src/services/          # API client
│   └── src/types/             # TypeScript types
│
├── backend/                     # Python FastAPI backend
│   ├── app/api/               # Route controllers
│   ├── app/models/            # Database models
│   ├── app/services/          # Business logic (optimizer)
│   ├── app/core/              # Configuration
│   └── seed.py                # Database seeding
│
├── Documentation
├── Docker configuration
└── Development tools
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+

### 1️⃣ Backend (terminal 1)
```bash
cd backend
pip install -r requirements.txt
python seed.py    # Load test data
python run.py      # Start server
```
Backend runs at: `http://localhost:8000`

### 2️⃣ Frontend (terminal 2)
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: `http://localhost:3000`

### 3️⃣ Access
- **Dashboard**: http://localhost:3000/dashboard
- **API Docs**: http://localhost:8000/docs

## 📚 Documentation

**Get Started:**
- **[PROJECT_STATUS.md](./PROJECT_STATUS.md)** - 📊 Executive summary & current status (START HERE!)
- **[GETTING_STARTED.md](./GETTING_STARTED.md)** - 5-minute setup guide

**For Users:**
- **[USER_GUIDE.md](./USER_GUIDE.md)** - Complete end-user walkthrough with visuals

**For Developers:**
- **[API_REFERENCE.md](./API_REFERENCE.md)** - All 34+ endpoints with curl examples
- **[SECURITY.md](./SECURITY.md)** - JWT authentication & security implementation
- **[FULL_ARCHITECTURE.md](./FULL_ARCHITECTURE.md)** - Detailed system architecture & integration
- **[PROJECT_ROADMAP.md](./PROJECT_ROADMAP.md)** - Complete timeline, phases, and forecasts
- **[DEVELOPMENT.md](./DEVELOPMENT.md)** - Developer workflow & contribution guide

## 🛠️ Tech Stack

**Frontend:**
- Next.js 14, React, TypeScript
- Tailwind CSS, Three.js
- axios HTTP client

**Backend:**
- FastAPI (Python)
- SQLAlchemy ORM
- Pydantic validation
- OpenAI API

**Database:**
- SQLite (development)
- PostgreSQL (production)

**Deployment:**
- Docker & Docker Compose

## 📋 API Endpoints

### Resources
- `GET/POST /api/projects/` - Projects
- `GET/POST /api/signatures/` - Signatures
- `GET/POST /api/datasets/` - Datasets
- `GET/POST /api/metrics/` - Metrics
- `GET/POST /api/programs/` - Programs

### Optimization
- `POST /api/optimization/run` - Start optimization
- `GET /api/optimization/runs` - List runs
- `GET /api/optimization/{id}` - Get run details
- `GET /api/optimization/{id}/variations` - Get variations
- `POST /api/optimization/{id}/stop` - Stop run

## 🎯 What's Included

- ✅ Full-featured API backend
- ✅ Modern responsive frontend
- ✅ Prompt optimization engine
- ✅ Multiple evaluation metrics
- ✅ Real-time progress monitoring
- ✅ Test data (seed script)
- ✅ Docker support
- ✅ Complete documentation
- ✅ TypeScript type safety
└── .github/          # GitHub workflows and configuration
```

## Quick Start

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python run.py
```

Backend API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

## Features

### Prompt Optimization Loop

The system implements an automated optimization loop:

1. **Signature**: Define the task contract (inputs/outputs)
2. **Program**: Execute the optimization logic
3. **Metric**: Measure success with custom metrics
4. **Dataset**: Provide input/output examples

### Frontend

- Modern landing page with WebGL effects using Three.js
- Admin dashboard for managing optimization tasks
- Real-time visualization of optimization progress
- Responsive design with Tailwind CSS

### Backend

- FastAPI REST API
- SQLAlchemy ORM for database operations
- OpenAI LLM integration for prompt variation
- Async optimization loop with background tasks
- Support for custom metrics and evaluation functions

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Three.js
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite (default) or PostgreSQL
- **LLM**: OpenAI API (optional, with fallback)

## API Endpoints

### Projects
- `GET /api/projects/` - List all projects
- `POST /api/projects/` - Create a new project
- `GET /api/projects/{id}` - Get project details
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Optimization
- `POST /api/optimization/run` - Start optimization run
- `GET /api/optimization/runs` - List optimization runs
- `GET /api/optimization/{id}` - Get run details
- `GET /api/optimization/{id}/variations` - Get prompt variations
- `POST /api/optimization/{id}/stop` - Stop optimization run

## Environment Variables

Create a `.env` file in the backend directory:

```
DATABASE_URL=sqlite:///./prompt_optimization.db
OPENAI_API_KEY=sk-...
```

## Development

### Adding Models

1. Update model definitions in `backend/app/models/database_models.py`
2. Update schemas in `backend/app/models/schemas.py`
3. Create API routes in `backend/app/api/`

### Extending Optimization

Edit `backend/app/services/optimizer.py` to:
- Add new metric types
- Implement custom evaluation logic
- Integrate different LLM providers

## License

MIT
