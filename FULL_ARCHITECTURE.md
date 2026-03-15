# 🏗️ Arquitetura Completa - Prompt Optimization Platform

## Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                     CLIENTE (BROWSER)                            │
│                    localhost:3000                                 │
└────────────────────────────┬────────────────────────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │  NEXT.JS FRONTEND │
                    │    REACT + TS     │
                    │  Authentication   │
                    │  State Management │
                    └─────────┬─────────┘
                              │ HTTPS/CORS
                    ┌─────────▼─────────────────┐
                    │   FASTAPI BACKEND         │
                    │   Python 3.11+            │
                    │   localhost:8000          │
┌───────────────────┤                           ├──────────────┐
│                   │  Layers:                  │              │
│                   │  ├─ API Router            │              │
│                   │  ├─ Services              │              │
│                   │  ├─ Database ORM          │              │
│                   │  └─ Authentication        │              │
│                   └───────┬───────────────────┘              │
│                           │                                   │
│       ┌───────────────────┼───────────────────┐              │
│       │                   │                   │              │
│   ┌───▼────┐   ┌─────┬───▼──┬─────┐  ┌──────▼──┐            │
│   │ SQLite │   │Auth │ Jobs │ LLM │  │  Cache  │            │
│   │ (Dev)  │   │Service │   │API  │  │ (Redis) │            │
│   └────────┘   └─────┴──────┴─────┘  └─────────┘ (Futuro)  │
│                                                               │
│   ┌──────────────────┐                                        │
│   │  PostgreSQL      │                                        │
│   │  (Production)    │                                        │
│   └──────────────────┘                                        │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## 1. Frontend Architecture

### Estrutura de Componentes
```
src/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home / Landing
│   ├── login/                   # Login page (novo)
│   ├── register/                # Register page (novo)
│   └── dashboard/
│       ├── layout.tsx           # Protected layout
│       ├── page.tsx             # Dashboard home
│       ├── projects/
│       │   └── [id]/
│       │       └── page.tsx     # Project detail
│       └── optimizations/
│           └── [id]/
│               └── page.tsx     # Optimization monitor
│
├── components/
│   ├── LandingPage.tsx          # Homepage com WebGL
│   ├── Canvas3D.tsx             # Three.js effects
│   ├── Dashboard.tsx            # Project list
│   ├── ProjectDetail.tsx        # Project CRUD
│   ├── OptimizationDetail.tsx   # Monitor real-time
│   ├── AuthGuard.tsx            # Route protection (novo)
│   └── UserMenu.tsx             # User profile menu (novo)
│
├── services/
│   ├── api.ts                   # Axios client
│   └── auth.ts                  # Auth utilities (novo)
│
├── types/
│   └── index.ts                 # TypeScript interfaces
│
└── styles/
    ├── globals.css
    └── dashboard.css
```

### Data Flow Frontend
```
User Action
    ↓
Event Handler (onClick, onChange)
    ↓
Component Event → useState/useReducer
    ↓
API Call (api.ts)
    ↓
HTTP Request + JWT Header
    ↓
Response/Error Handling
    ↓
State Update → Re-render
```

## 2. Backend Architecture

### Camadas de Aplicação
```
backend/
├── app/
│   ├── main.py                  # Application entry point
│   │
│   ├── api/                     # Route controllers
│   │   ├── auth.py             # Login, Register, JWT
│   │   ├── projects.py         # CRUD Projects
│   │   ├── signatures.py       # CRUD Signatures
│   │   ├── datasets.py         # CRUD Datasets
│   │   ├── metrics.py          # CRUD Metrics
│   │   ├── programs.py         # CRUD Programs
│   │   └── optimization.py     # Optimization runs
│   │
│   ├── models/
│   │   ├── database_models.py  # SQLAlchemy models
│   │   │   ├── User
│   │   │   ├── Project
│   │   │   ├── Signature
│   │   │   ├── Dataset
│   │   │   ├── Metric
│   │   │   ├── Program
│   │   │   ├── OptimizationRun
│   │   │   └── PromptVariation
│   │   │
│   │   └── schemas.py          # Pydantic request/response
│   │
│   ├── services/
│   │   ├── optimizer.py        # Core optimization engine
│   │   ├── auth_service.py     # JWT & authentication
│   │   └── llm_service.py      # LLM API integration
│   │
│   └── core/
│       ├── database.py         # DB connection & session
│       ├── security.py         # Password hashing & JWT
│       └── config.py           # Environment variables
│
├── seed.py                      # Database initialization
├── run.py                       # Server entry point
├── requirements.txt             # Dependencies
└── .env.example                 # Environment template
```

### Request Flow Backend
```
HTTP Request
    ↓
↓──── Middleware ────────────────┐
│  ├─ CORS validation            │
│  ├─ Request logging            │
│  └─ Error handling             │
│                                │
├─ Route Handler (Router)        │
│  ├─ Path matching              │
│  └─ Method validation          │
│                                │
├─ Authentication (Dependency)   │
│  ├─ Extract JWT token          │
│  ├─ Verify signature           │
│  └─ Get current user           │
│                                │
├─ Validation (Pydantic)         │
│  ├─ Request body schema        │
│  └─ Type checking              │
│                                │
├─ Business Logic (Service)      │
│  ├─ Database queries           │
│  ├─ Algorithm processing       │
│  └─ External API calls         │
│                                │
├─ Database Operation            │
│  ├─ Before: Validate data      │
│  ├─ Execute: Run transaction   │
│  └─ After: Commit/rollback     │
│                                │
├─ Response Preparation          │
│  ├─ Serialize (Pydantic)       │
│  ├─ Status code                │
│  └─ Headers                    │
│                                │
└──────────────────────────────────┘
                ↓
        HTTP Response
```

## 3. Database Architecture

### Entity Relationship Diagram
```
┌─────────────┐
│    USER     │ (novo)
├─────────────┤
│ id (PK)     │
│ email       │
│ name        │
│ password    │
│ is_admin    │
└──────┬──────┘
       │ owns
       │ (1:N)
       ↓
┌──────────────────────┐
│    PROJECT           │
├──────────────────────┤
│ id (PK)              │
│ user_id (FK)         │
│ name                 │
│ description          │
│ created_at           │
└──────┬───────────────┘
       │ (1:N) contains
       ├──────────────────────┬─────────────────┬─────────────────┐
       ↓                      ↓                 ↓                 ↓
┌─────────────┐    ┌─────────────┐   ┌──────────────┐   ┌──────────────┐
│ SIGNATURE   │    │  DATASET    │   │   METRIC     │   │   PROGRAM    │
├─────────────┤    ├─────────────┤   ├──────────────┤   ├──────────────┤
│ id (PK)     │    │ id (PK)     │   │ id (PK)      │   │ id (PK)      │
│ project_id  │    │ project_id  │   │ project_id   │   │ project_id   │
│ name        │    │ signature_id│   │ signature_id │   │ signature_id │
│ input[]     │    │ examples    │   │ metric_type  │   │ code         │
│ output[]    │    │ created_at  │   │ config       │   │ created_at   │
└─────────────┘    └─────────────┘   └──────────────┘   └──────────────┘
       │
       │ (1:N) uses
       ↓
┌──────────────────────────┐
│   OPTIMIZATION_RUN       │
├──────────────────────────┤
│ id (PK)                  │
│ project_id (FK)          │
│ signature_id (FK)        │
│ metric_id (FK)           │
│ program_id (FK)          │
│ status                   │
│ best_score               │
│ best_prompt              │
│ current_iteration        │
│ created_at               │
└────────┬─────────────────┘
         │ (1:N) contains
         ↓
┌──────────────────┐
│ PROMPT_VARIATION │
├──────────────────┤
│ id (PK)          │
│ run_id (FK)      │
│ prompt           │
│ score            │
│ iteration        │
│ is_best          │
└──────────────────┘
```

### Índices Otimizados
```python
# Consultas frequentes
- User.email (unique, index)
- Project.user_id (index)
- Signature.project_id (index)
- Dataset.project_id (index)
- Metric.project_id (index)
- Program.project_id (index)
- OptimizationRun.project_id (index)
- OptimizationRun.status (index)
- PromptVariation.run_id (index)
```

## 4. Fluxo de Otimização

### Processo Passo-a-Passo
```
User clica "Iniciar Nova Otimização"
        ↓
Frontend abre modal/form
        ↓
User entra prompt inicial: "You are helpful..."
        ↓
POST /api/optimization/run
├─ Validar: projeto, signature, dataset, métrica, programa
├─ Criar OptimizationRun com status="running"
└─ Iniciar background task
        ↓
Backend: Otimizador começa
        ↓
ITERAÇÃO 1 (de 5):
├─ Avaliar prompt inicial no dataset
├─ Score: 45%
├─ Gerar 3 variações com LLM:
│  ├─ V1: "You are professional..." → Score: 52%
│  ├─ V2: "You are empathetic..." → Score: 58% ← MELHOR
│  └─ V3: "You are friendly..." → Score: 50%
├─ Guardar V2 como best_prompt
└─ Salvar scores no BD
        ↓
ITERAÇÃO 2-5: Repetir com base em V2
        ↓
Todos os scores atualizam em tempo real no frontend
        ↓
OptimizationDetail.tsx auto-refresh a cada 3 segundos
        ↓
Usuário vê:
├─ Status: running → completed
├─ Score: 45% → 85%
├─ All variations list
└─ Best prompt encontrado
        ↓
Usuário pode copiar/usar best prompt
```

## 5. Integração Frontend-Backend

### Exemplo: Criar Projeto
```
FRONTEND:

1. User preenche form:
   name: "Translation Optimizer"
   description: "Optimize translation prompts"

2. onClick "Criar":
   POST /api/projects
   Body: { name, description }
   Headers: { Authorization: Bearer <token> }

3. Response:
   {
     "id": 1,
     "user_id": 5,
     "name": "Translation Optimizer",
     "created_at": "2024-01-15T10:30:00"
   }

4. Frontend:
   - setState({ projects: [...projects, newProject] })
   - Router.push(`/dashboard/projects/${id}`)


BACKEND:

1. Request hits POST /api/projects/

2. Dependency injection:
   - Extrair token JWT
   - get_current_user() → User(id=5)
   - get_db() → Session

3. Pydantic validation:
   - ProjectCreate schema
   - name field required
   - description optional

4. Business logic:
   - Criar instância Project
   - projeto.user_id = 5 (do token)
   - db.add(projeto)
   - db.commit()

5. Response:
   - Status 201 Created
   - ProjectResponse schema
   - JSON serializado
```

## 6. Comunicação HTTP

### Exemplo: Listar Projetos
```bash
# Frontend → Backend
GET http://localhost:8000/api/projects
Headers:
  Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
  Content-Type: application/json

# Backend → Frontend (200 OK)
[
  {
    "id": 1,
    "user_id": 5,
    "name": "Customer Service Optimization",
    "description": "Optimize support prompts",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

## 7. Escalabilidade & Performance

### Otimizações Implementadas
```
1. Frontend:
   ✅ Code splitting (Next.js)
   ✅ Image optimization (next/image)
   ✅ Lazy loading (React.lazy)
   ✅ Caching API responses
   ✅ Minimize re-renders

2. Backend:
   ✅ Database indexes
   ✅ Async/await para I/O
   ✅ Connection pooling
   ✅ Pagination para listas
   ✅ Background tasks (long-running)

3. Futuro:
   ⏳ Redis cache layer
   ⏳ WebSocket para real-time
   ⏳ Load balancing
   ⏳ CDN para static assets
   ⏳ Database sharding
```

### Limites Atuais
```
- MAX_PROJECTS_PER_USER: Unlimited (add DB limit)
- MAX_VARIATIONS_PER_ITERATION: 3
- MAX_ITERATIONS: 5
- ITERATION_TIMEOUT: 5 minutes
- OPTIMIZATION_TIMEOUT: 30 minutes
```

## 8. Deployment Architecture

### Development (Atual)
```
localhost:3000  ← Frontend (localhost)
localhost:8000  ← Backend (localhost)
SQLite          ← Database (file-based)
```

### Production (Recomendado)
```
┌─────────────────────────────────────┐
│         NGINX Reverse Proxy          │
│         (SSL/TLS)                    │
│         Port 443/80                  │
└────────────┬────────────────────────┘
             │
    ┌────────┴──────────┐
    ↓                   ↓
┌────────────┐    ┌──────────────┐
│ Frontend   │    │ Backend      │
│ Next.js    │    │ FastAPI      │
│ Node.js    │    │ Python       │
│ Port 3000  │    │ Port 8000    │
└────────────┘    └─────┬────────┘
                        │
                   ┌────▼─────┐
                   │PostgreSQL │
                   │Port 5432  │
                   └───────────┘
                   
With Docker Compose:
- 3 containers (frontend, backend, postgres)
- Shared network
- Volume persistence
- Environment variables
```

## 9. Segurança em Produção

```
✅ HTTPS/TLS (Nginx certificate)
✅ JWT authentication
✅ CORS whitelist
✅ Rate limiting
✅ SQL injection prevention
✅ XSS protection
✅ CSRF tokens
✅ Password hashing (bcrypt)
✅ Environment variables (no secrets in code)
✅ Database encryption
✅ Regular backups
```

## 10. Monitoramento & Logging

### Logs Estruturados
```python
# Backend logging
logger.info("Optimization started", {
    "run_id": 1,
    "project_id": 1,
    "user_id": 5,
    "timestamp": "2024-01-15T10:30:00"
})

logger.error("Optimization failed", {
    "error": "OpenAI API timeout",
    "run_id": 1,
    "retry_count": 3
})
```

### Métricas para Rastrear
- Response time (average, P95, P99)
- Error rate (4xx, 5xx)
- Database query time
- API call latency (LLM)
- Optimization success rate
- User count & growth

---

## Resumo da Integração

| Componente | Tecnologia | Responsabilidade |
|-----------|-----------|---|
| Frontend | Next.js 14 | UI, Forms, Real-time updates |
| Backend API | FastAPI | Routes, Validation, Business logic |
| Authentication | JWT + bcrypt | User sessions, Security |
| Database | SQLite/PostgreSQL | Data persistence |
| LLM Integration | OpenAI API | Prompt generation |
| Background Jobs | asyncio | Long-running tasks |
| Real-time | Polling (atual) | WebSocket (futuro) |

---

**Esta arquitetura é:**
- ✅ Escalável (pode crescer com cache, async workers, sharding)
- ✅ Segura (JWT, validação, hasheamento)
- ✅ Produção-ready (Docker, env variables, error handling)
- ✅ Documentada (este arquivo)
- ✅ Testável (separation of concerns)
