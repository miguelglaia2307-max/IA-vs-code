# 🔐 Sistema de Segurança - Prompt Optimization Platform

## 1. Autenticação & Autorização

### Implementação JWT

#### Backend - Modelo de Usuário
```python
# backend/app/models/database_models.py - Adicionar

from sqlalchemy import Column, String, Boolean
from datetime import datetime
from passlib.context import CryptContext

# Hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)
    
    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)
```

#### Backend - Endpoints de Autenticação
```python
# backend/app/api/auth.py - NOVO ARQUIVO

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Configurações
SECRET_KEY = "sua-chave-secreta-muito-segura"  # Usar variável de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int

class LoginRequest(BaseModel):
    email: str
    password: str

class RegisterRequest(BaseModel):
    email: str
    name: str
    password: str

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Extrair usuário do JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return user

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Endpoint de login"""
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not user.verify_password(request.password):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    
    # Gerar token
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user.id), "exp": expires}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "user_id": user.id
    }

@router.post("/register", response_model=TokenResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Endpoint de registro"""
    # Verificar se email já existe
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(status_code=400, detail="Email já registrado")
    
    # Criar usuário
    user = User(email=request.email, name=request.name)
    user.set_password(request.password)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Gerar token
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user.id), "exp": expires}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "user_id": user.id
    }

@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Obter informações do usuário logado"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "is_admin": current_user.is_admin
    }
```

### Frontend - Login Page
```typescript
// frontend/src/pages/LoginPage.tsx

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { api } from '@/services/api'

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const response = await api.post('/auth/login', {
        email,
        password
      })
      
      // Armazenar token
      localStorage.setItem('auth_token', response.data.access_token)
      localStorage.setItem('user_id', response.data.user_id)
      
      // Redirecionar para dashboard
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erro ao fazer login')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-dark">
      <div className="w-full max-w-md p-8 bg-dark-secondary rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold mb-6 text-cyan-400">Login</h1>
        
        {error && (
          <div className="mb-4 p-4 bg-red-500/20 border border-red-500 rounded">
            {error}
          </div>
        )}
        
        <form onSubmit={handleLogin}>
          <div className="mb-4">
            <label className="block text-white mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2 bg-dark border border-cyan-400/30 rounded text-white"
              required
            />
          </div>
          
          <div className="mb-6">
            <label className="block text-white mb-2">Senha</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-4 py-2 bg-dark border border-cyan-400/30 rounded text-white"
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full px-4 py-2 bg-cyan-500 hover:bg-cyan-600 text-dark font-bold rounded disabled:opacity-50"
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
      </div>
    </div>
  )
}
```

### Frontend - Setup de Token
```typescript
// frontend/src/services/api.ts - MODIFICAÇÃO

import axios from 'axios'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
})

// Interceptor para adicionar token em todas as requisições
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Interceptor para redirecionar se token expirou
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export { api }
```

## 2. Proteção de Recursos

### Backend - Proteger Endpoints
```python
# backend/app/api/projects.py - MODIFICAÇÃO

from fastapi import Depends
from app.core.database import get_db
from app.models.database_models import User

@router.get("/")
def list_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Listar projetos do usuário logado"""
    projects = db.query(Project).filter(
        Project.user_id == current_user.id
    ).all()
    return projects

@router.post("/")
def create_project(
    request: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Criar novo projeto (usuário autenticado)"""
    project = Project(
        **request.dict(),
        user_id=current_user.id
    )
    db.add(project)
    db.commit()
    return project
```

### Frontend - Rota Protegida
```typescript
// frontend/src/app/dashboard/layout.tsx - NOVO

'use client'

import { useRouter } from 'next/navigation'
import { useEffect, useState } from 'react'

export default function DashboardLayout({
  children
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      router.push('/login')
    } else {
      setIsAuthenticated(true)
    }
  }, [router])

  if (!isAuthenticated) {
    return <div>Carregando...</div>
  }

  return <>{children}</>
}
```

## 3. Variáveis de Ambiente Seguras

### Backend - .env
```
# Segurança
SECRET_KEY=sua-chave-secreta-muito-segura-e-aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Banco de dados
DATABASE_URL=sqlite:///./data.db
# Ou PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# API OpenAI
OPENAI_API_KEY=sk-...

# Configuração
DEBUG=false
ENVIRONMENT=production
```

### Frontend - .env.local
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 4. CORS & Segurança de Comunicação

### Backend - CORS Configuração
```python
# backend/app/main.py

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3000/",
        "https://seu-dominio.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 5. Rate Limiting (Futuro)

```python
# Prevenir abuso
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@router.post("/api/auth/login")
@limiter.limit("5/minute")
def login(request, background_tasks):
    # Máximo 5 tentativas de login por minuto
    pass
```

## 6. Validação de Entrada

```python
# Validar todos os inputs com Pydantic
from pydantic import EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr  # Valida email
    password: str = Field(..., min_length=8, max_length=100)
    name: str = Field(..., min_length=1, max_length=100)
```

## 7. SQL Injection Prevention

✅ **Automático com SQLAlchemy ORM**
```python
# SEGURO - Usa parameterized queries
user = db.query(User).filter(User.email == email).first()

# NUNCA faça isso
# user = db.query(User).filter(f"email = '{email}'").first()
```

## 8. Checklist de Segurança

- ✅ Endpoints protegidos com JWT
- ✅ Senhas hasheadas com bcrypt
- ✅ CORS configurado
- ✅ Validação de entrada com Pydantic
- ✅ SQL Injection prevention
- ✅ Token expiration
- ✅ Variáveis de ambiente não committed
- ✅ HTTPS em produção (usar nginx/reverse proxy)

## 9. Deploy Seguro

```yaml
# docker-compose.yml - PRODUÇÃO

services:
  backend:
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - DATABASE_URL=postgresql://user:${DB_PASSWORD}@postgres:5432/optim
      - DEBUG=false
    restart: always
```

---

**Próximos passos de segurança:**
1. Implementar 2FA (Two Factor Authentication)
2. Adicionar refresh tokens
3. Implementar rate limiting
4. Configurar HTTPS/SSL
5. Adicionar audit logging
6. Implementar RBAC (Role Based Access Control)
