# Frontend-Backend Integration & AI Error Recovery - Setup Guide

## ✅ What Has Been Integrated

### 1. **Frontend-Backend Connection**
- ✅ Frontend (Next.js) running on `http://localhost:3000`
- ✅ Backend (FastAPI) running on `http://localhost:8000`
- ✅ CORS configured for cross-origin requests
- ✅ Authentication tokens passed in headers
- ✅ Axios client configured with base URL
- ✅ All API endpoints accessible from frontend

### 2. **Active AI Error Recovery Agent**
- ✅ Centralized error logging system
- ✅ OpenAI GPT-3.5 integration for error analysis
- ✅ Automatic error tracking and reporting
- ✅ Real-time monitoring dashboard
- ✅ AI-powered fix suggestions
- ✅ Error pattern detection

### 3. **Error Handling Infrastructure**
- ✅ Global error handler middleware
- ✅ JSON logging with timestamps
- ✅ Python traceback capture
- ✅ Frontend error reporter with backlog
- ✅ Health check endpoint for AI service

## 🚀 Quick Start

### 1. **Set OpenAI API Key**
Edit `backend/.env`:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 2. **Start Both Servers**
```bash
# Terminal 1: Frontend
cd frontend
npm run dev

# Terminal 2: Backend
cd backend
python run.py
```

### 3. **Access the Application**
- **App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Monitoring**: http://localhost:3000/dashboard/monitoring (after login)

### 4. **Test the Integration**

**Option A: Create a test account**
1. Go to `http://localhost:3000/register`
2. Sign up with test account
3. Login to dashboard
4. Click "System Monitoring" button

**Option B: Test via API**
```bash
# Register user
$body = @{
    email = "test@example.com"
    username = "testuser"
    password = "password123"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri http://localhost:8000/api/auth/register `
  -Method POST `
  -ContentType "application/json" `
  -Body $body

$token = ($response | ConvertFrom-Json).access_token

# Test monitoring endpoint
Invoke-WebRequest -Uri http://localhost:8000/api/monitoring/dashboard `
  -Headers @{Authorization = "Bearer $token"}
```

## 📊 Monitoring Dashboard Features

Access at: `http://localhost:3000/dashboard/monitoring`

Shows:
- **Total Recent Errors**: Count of errors in the last period
- **Error Types**: Breakdown of different error categories
- **AI Agent Status**: Health check of the error recovery service
- **Error History**: Last 10 errors with context and timestamps
- **Auto-Refresh**: Updates every 10 seconds

## 🔧 How Error Recovery Works

### 1. **Error Occurs**
```
User Action → Frontend Error → Caught by Global Handler
```

### 2. **Error Logged**
```
Error → Backend Logger → JSON File (errors.jsonl)
```

### 3. **AI Analysis**
```
Logged Error → OpenAI GPT-3.5 → Root Cause Analysis
```

### 4. **Dashboard Display**
```
Analyzed Error → Database → Monitoring Dashboard
```

## 📝 Error Log Files

Located in `backend/logs/`:
- **app.log**: Full application logs
- **errors.jsonl**: JSON error records (one per line)

### Example Error Entry
```json
{
  "timestamp": "2026-03-14T13:02:59.123456",
  "type": "ValidationError",
  "message": "Invalid email format",
  "context": {
    "source": "user_input",
    "field": "email"
  },
  "traceback": "Traceback (most recent call last):\n  File \"app.py\", line 42..."
}
```

## 🔌 API Endpoints Reference

### Authentication
```
POST /api/auth/register    - Create account
POST /api/auth/login       - Login
GET  /api/auth/me          - Get current user
```

### Monitoring & Error Recovery
```
POST /api/monitoring/errors/report           - Report error
GET  /api/monitoring/errors/recent           - Get recent errors
POST /api/monitoring/errors/analyze          - AI analysis
POST /api/monitoring/errors/fix-suggestion   - Get fix
GET  /api/monitoring/health/ai-agent         - Check AI status
GET  /api/monitoring/dashboard               - Dashboard data
```

### Project Management
```
GET  /api/projects/                - List projects
POST /api/projects/                - Create project
GET  /api/projects/{id}            - Get project
PUT  /api/projects/{id}            - Update project
DELETE /api/projects/{id}          - Delete project
```

## 🛡️ Security Notes

1. **Authentication Required**: Monitoring endpoints require valid JWT token
2. **CORS**: Configured for localhost development
3. **Error Sanitization**: Implement in production to avoid leaking sensitive data
4. **Rate Limiting**: Not implemented - add for production
5. **Admin Only**: Restrict monitoring to admin users in production

## 🔍 Troubleshooting

### Backend not responding
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill if necessary and restart
```

### AI Agent showing "Offline"
- Check `.env` has valid `OPENAI_API_KEY`
- Verify API key is correct: `https://platform.openai.com/api_keys`
- Check internet connectivity

### Frontend can't connect to backend
- Verify both servers are running
- Check CORS settings in `backend/app/main.py`
- Ensure ports are correct (3000 and 8000)

### Errors not appearing in dashboard
- Check `backend/logs/errors.jsonl` exists
- Verify error reporter is initialized in frontend
- Check browser console for errors

## 📈 Next Steps

### For Development
1. Test error scenarios manually
2. Add more comprehensive logging
3. Implement dashboard persistence
4. Add email alerts for critical errors

### For Production
1. Implement admin authentication
2. Add rate limiting on error endpoints
3. Move to PostgreSQL database
4. Implement Sentry integration
5. Add CI/CD pipeline monitoring
6. Set up log rotation
7. Implement error aggregation

## 📚 Documentation Files

- `ERROR_RECOVERY_GUIDE.md` - Detailed error recovery system guide
- `DEVELOPMENT.md` - Development setup
- `API_REFERENCE.md` - Full API documentation
- `ARCHITECTURE.md` - System design overview

## ✨ Key Features Summary

| Feature | Status | Notes |
|---------|--------|-------|
| Frontend-Backend Connected | ✅ | Both running, CORS configured |
| User Authentication | ✅ | JWT tokens, bcrypt passwords |
| Error Logging | ✅ | JSON format, traceback included |
| AI Error Analysis | ⚠️ | Requires OPENAI_API_KEY |
| Monitoring Dashboard | ✅ | Real-time, auto-refresh |
| Error Reporting | ✅ | Frontend to backend integration |
| Health Checks | ✅ | Endpoints for both services |

## 🎯 Demo Workflow

1. **Register Account**: http://localhost:3000/register
2. **Login**: http://localhost:3000/login
3. **View Dashboard**: http://localhost:3000/dashboard
4. **Open Monitoring**: Click "System Monitoring" button
5. **Trigger Error** (optional): Use browser console to throw test error
6. **Check Monitoring Dashboard**: Error will appear in real-time
7. **View AI Analysis**: Click error for AI-generated analysis

---

**Current Status**: Frontend & Backend fully integrated with active AI Error Recovery Agent ✨
