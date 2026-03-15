# Prompt Optimization Platform - Project Instructions

## Project Overview
A full-stack platform for automated prompt optimization with a modern landing page featuring WebGL effects similar to igloo.inc.

The system implements an optimization loop:
- **Signature**: Define the task contract (inputs/outputs)
- **Program**: Execute the optimization logic
- **Metric**: Measure success
- **Dataset**: Provide input/output examples

The optimizer generates prompt variations, tests them, measures results, and converges to the best solution automatically.

## Architecture

### Frontend (Next.js)
- Modern landing page with Three.js WebGL effects
- Admin dashboard for managing optimization tasks
- Real-time visualization of optimization progress

### Backend (Python FastAPI)
- Optimization loop engine
- Signature/Program/Metric/Dataset management
- Integration with LLMs (OpenAI, etc.)
- Results tracking and metrics

## Tech Stack
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Three.js
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy, Pydantic
- **Database**: PostgreSQL/SQLite
- **Deployment**: Docker, Docker Compose

## Development Instructions
1. Navigate to frontend directory and run: `npm install && npm run dev`
2. Navigate to backend directory and run: `pip install -r requirements.txt && python app.py`
3. Frontend will be available at http://localhost:3000
4. Backend API will be available at http://localhost:8000
