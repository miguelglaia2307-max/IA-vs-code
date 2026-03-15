# 🚀 Production Deployment Guide

## 📋 Pré-requisitos

- Docker & Docker Compose 2.0+
- PostgreSQL 16+
- Redis 7+
- OpenAI API key
- Domain name com SSL
- Cloud provider: AWS, Google Cloud, Azure, ou DigitalOcean

---

## 🏗️ Arquitetura de Produção

```
Internet
    ↓
(Load Balancer - CloudFlare/AWS)
    ↓
Nginx (Reverse Proxy)
    ├─ Frontend (Next.js)
    └─ Backend (FastAPI)
    ├─ /api → Backend
    ├─ / → Frontend
    ├─ /flower → Celery Flower Monitoring
    └─ /prometheus → Metrics
         ↓
PostgreSQL (Database)
         ↓
Redis (Cache & Message Broker)
         ↓
Celery Workers (Async Jobs)
```

---

## 🔧 Configuração Inicial

### 1. Clonar o repositório

```bash
git clone https://github.com/miguelglaia2307-max/IA-vs-code.git
cd IA-vs-code
```

### 2. Preparar arquivo .env.production

```bash
cp .env.production.example .env.production

# Editar com seus valores
nano .env.production

# Valores críticos a mudar:
- POSTGRES_PASSWORD (senha forte)
- OPENAI_API_KEY (sua chave da OpenAI)
- SECRET_KEY (gerar com: python -c "import secrets; print(secrets.token_urlsafe(32))")
- ALLOWED_ORIGINS (seu domínio)
```

### 3. Gerar chaves seguras

```bash
# SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# REDIS_PASSWORD
python3 -c "import secrets; print(secrets.token_hex(32))"

# PostgreSQL super user password
pwgen -s 32 1
```

---

## 🐳 Deploy com Docker Compose

### Build e Start

```bash
# Build todas as imagens
docker-compose -f docker-compose.prod.yml build

# Iniciar os serviços
docker-compose -f docker-compose.prod.yml up -d

# Verificar status
docker-compose -f docker-compose.prod.yml ps

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend
docker-compose -f docker-compose.prod.yml logs -f celery_worker
```

### Database Migrations

```bash
# Executar migrations
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Seed data (opcional)
docker-compose -f docker-compose.prod.yml exec backend python seed.py
```

---

## 🌐 Nginx Configuration

Arquivo `nginx.conf` deve incluir:

```nginx
upstream backend {
    server backend:8000;
}

upstream frontend {
    server frontend:3000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirecionar para HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Certificates (use Let's Encrypt)
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_cache_bypass $http_upgrade;
    }

    # API Backend
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Flower Monitoring (restrito)
    location /flower/ {
        proxy_pass http://flower:5555/;
        # Adicionar autenticação aqui
    }
}
```

---

## 📊 Monitoramento & Observabilidade

### 1. Flower (Celery Monitoring)

```
http://yourdomain.com/flower
```

### 2. Prometheus Metrics

```
http://yourdomain.com:8001/metrics
```

### 3. API Documentation

```
http://yourdomain.com/api/docs  (Swagger)
```

### 4. Health Checks

```bash
curl http://yourdomain.com/api/health
```

---

## 🔒 Segurança em Produção

### 1. SSL/TLS com Let's Encrypt

```bash
# Using Certbot
docker run --rm -it -v "/etc/letsencrypt:/etc/letsencrypt" \
    -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
    -p 80:80 \
    certbot/certbot certonly --standalone -d yourdomain.com
```

### 2. Environment Variables Seguros

- ✅ Usar `.env.production` com permissões 600
- ✅ Não commitar `.env.production` no Git
- ✅ Usar AWS Secrets Manager ou similar em produção
- ✅ Rotacionar secrets regularmente

### 3. Firewall Rules

```bash
# Permitir apenas:
- 80 (HTTP)
- 443 (HTTPS)
- 22 (SSH - de IPs específicos)

# Bloquear:
- 5432 (PostgreSQL)
- 6379 (Redis)
- 8001 (Prometheus)
- 5555 (Flower)
```

### 4. Database Security

```sql
-- Criar usuário restrito
CREATE USER app_user WITH PASSWORD 'strong_password';
CREATE DATABASE prompt_optimization OWNER app_user;

-- Denegar acesso público
REVOKE ALL ON DATABASE postgres FROM public;
```

---

## 📈 Scaling & Performance

### Horizontal Scaling

```bash
# Múltiplos backend workers
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# Múltiplos celery workers
docker-compose -f docker-compose.prod.yml up -d --scale celery_worker=5
```

### Otimizações

1. **Frontend Caching**
   ```nginx
   location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|webp)$ {
       expires 1y;
       add_header Cache-Control "public, immutable";
   }
   ```

2. **Backend Connection Pooling**
   - Usar SQLAlchemy pooling
   - Configurar max_overflow e pool_size

3. **Redis Persistence**
   - Ativar AOF (Append-Only File)
   - Backups regulares

---

## 🚨 Backup & Disaster Recovery

### Database Backup

```bash
# Backup diário
docker-compose -f docker-compose.prod.yml exec postgres \
    pg_dump -U prompt_user prompt_optimization > backup_$(date +%Y%m%d).sql

# Restaurar
docker-compose -f docker-compose.prod.yml exec postgres \
    psql -U prompt_user prompt_optimization < backup_20260315.sql
```

### Automated Backups

```bash
# Adicionar a crontab
0 2 * * * docker-compose -f /path/to/docker-compose.prod.yml exec postgres \
    pg_dump -U prompt_user prompt_optimization > /backups/db_$(date +\%Y\%m\%d).sql
```

---

## 📋 Checklist de Deploy

- [ ] Arquivo `.env.production` criado e preenchido
- [ ] Secrets gerados (SECRET_KEY, REDIS_PASSWORD, etc)
- [ ] SSL certificates configurados
- [ ] PostgreSQL database criado
- [ ] Redis inicializado
- [ ] Docker images built
- [ ] Containers iniciados
- [ ] Database migrations executadas
- [ ] Health checks passando
- [ ] API `/health` respondendo
- [ ] Frontend acessível
- [ ] Nginx configurado e testado
- [ ] Monitoring ativado (Prometheus, Flower)
- [ ] Backups configurados
- [ ] Logs centralizados
- [ ] Alertas setup

---

## 🐛 Troubleshooting

### Backend não inicia

```bash
docker-compose -f docker-compose.prod.yml logs backend
# Procurar por erros de conexão ao PostgreSQL
```

### Redis connection refused

```bash
docker-compose -f docker-compose.prod.yml logs redis
# Verificar REDIS_PASSWORD está correto
```

### Frontend 404 errors

```bash
# Verificar nginx configuration
docker-compose -f docker-compose.prod.yml logs nginx

# Verificar Next.js build
docker-compose -f docker-compose.prod.yml logs frontend
```

### Celery workers não processando tasks

```bash
# Verificar broker connection
docker-compose -f docker-compose.prod.yml logs celery_worker

# Health check
curl http://yourdomain.com:8000/api/health/celery
```

---

## 📞 Support & Monitoring URLs

| Serviço | URL | Auth |
|---------|-----|------|
| Frontend | https://yourdomain.com | Public |
| API Docs | https://yourdomain.com/api/docs | Public |
| Flower | https://yourdomain.com/flower | ⚠️ Proteger |
| Prometheus | https://yourdomain.com:8001 | ⚠️ Proteger |
| Health Check | https://yourdomain.com/api/health | Public |

---

Parabéns! 🎉 Seu projeto está em produção!
