# Quick Start Guide

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.11+ (for backend)
- npm or yarn (for frontend package management)
- pip (for Python package management)

## Installation

### 1. Frontend Setup

Navigate to the frontend directory:
```bash
cd frontend
```

Install dependencies:
```bash
npm install
```

### 2. Backend Setup

Navigate to the backend directory:
```bash
cd backend
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

(Optional) Create a `.env` file with your configuration:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key if you want to use the LLM features:
```
OPENAI_API_KEY=sk-your-api-key-here
```

## Running the Application

### Option 1: Run Frontend Only (for UI development)
```bash
cd frontend
npm run dev
```
Frontend available at: `http://localhost:3000`

### Option 2: Run Backend Only (for API development)
```bash
cd backend
python run.py
```
Backend API available at: `http://localhost:8000`
API Documentation (Swagger): `http://localhost:8000/docs`

### Option 3: Run Both Together

From the root directory:
```bash
npm run dev
```

Or use VS Code Tasks (press Ctrl+Shift+D, then select "Full Stack" debug configuration)

## Project Structure

```
project-root/
├── frontend/              # Next.js React frontend
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   ├── components/   # React components
│   │   └── styles/       # Global styles
│   ├── package.json
│   └── tsconfig.json
│
├── backend/               # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Database & config
│   │   ├── models/      # Data models & schemas
│   │   ├── services/    # Business logic
│   │   └── main.py      # FastAPI app
│   ├── requirements.txt
│   └── run.py          # Entry point
│
├── .github/
│   └── copilot-instructions.md
└── README.md
```

## Key Features

### Frontend
- **Landing Page**: Beautiful WebGL-powered interface with Three.js
- **Dashboard**: Manage optimization projects (to be implemented)
- **Real-time Updates**: WebSocket support for live optimization progress (to be implemented)

### Backend
- **Prompt Optimization Loop**: Automated prompt improvement
- **Signature Management**: Define task contracts
- **Dataset Management**: Upload and manage examples
- **Metric Definition**: Create custom evaluation metrics
- **LLM Integration**: OpenAI API for prompt generation
- **REST API**: Full API for all operations

## API Endpoints

### Projects
- `POST /api/projects/` - Create project
- `GET /api/projects/` - List projects
- `GET /api/projects/{id}` - Get project details
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Optimization
- `POST /api/optimization/run` - Start optimization
- `GET /api/optimization/runs` - List runs
- `GET /api/optimization/{id}` - Get run details
- `GET /api/optimization/{id}/variations` - Get prompt variations
- `POST /api/optimization/{id}/stop` - Stop optimization

## Development with VS Code

### Recommended Extensions
- Python
- Pylance
- ESLint
- Prettier
- REST Client

### Using VS Code Tasks
Press `Ctrl+Shift+B` to see available build tasks:
- Start Frontend Dev Server
- Start Backend Dev Server
- Build Frontend
- Install Backend Dependencies
- Run Both Servers

### Using Debug Configuration
Press `Ctrl+Shift+D` and select:
- "Next.js Frontend" - Debug frontend with Node.js debugger
- "Python Backend" - Debug backend with Python debugger
- "Full Stack" - Debug both simultaneously

## Docker Support

Build and run with Docker Compose:
```bash
docker-compose up
```

This will start both frontend and backend services.

## Troubleshooting

### Frontend Issues
- Clear node_modules: `rm -rf node_modules && npm install`
- Clear .next cache: `rm -rf .next`
- Check Node version: `node --version`

### Backend Issues
- Create virtual environment: `python -m venv venv`
- Activate venv: `. venv/Scripts/activate` (Windows) or `source venv/bin/activate` (Unix)
- Reinstall packages: `pip install -r requirements.txt --force-reinstall`

### Database Issues
- Delete database file: `rm prompt_optimization.db`
- Tables will be recreated automatically on next run

## Next Steps

1. **Explore the UI**: Open `http://localhost:3000` and check out the landing page
2. **Read API Docs**: Visit `http://localhost:8000/docs` for interactive API documentation
3. **Create a Project**: Use the API to create your first optimization project
4. **Set up OpenAI**: Add your API key to use LLM-powered prompt generation

## Support

For issues and questions, check the main README.md file.
