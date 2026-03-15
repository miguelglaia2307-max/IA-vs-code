# AI Error Recovery System - Integration Guide

## Overview

The Prompt Optimization Platform now includes an **active AI Error Recovery Agent** that:
- ✅ Monitors all errors in real-time
- ✅ Analyzes errors using OpenAI GPT-3.5
- ✅ Suggests fixes and root cause analysis
- ✅ Tracks error patterns and trends
- ✅ Provides a monitoring dashboard

## System Architecture

```
┌─────────────────────┐
│   Frontend (Next.js) │
│  Error Reporter     │
└──────────┬──────────┘
           │ (HTTP)
           ▼
┌─────────────────────────────────────────┐
│         Backend (FastAPI)               │
├─────────────────────────────────────────┤
│ Error Handler Middleware                │
│ ↓                                       │
│ Central Logger (logs/errors.jsonl)     │
│ ↓                                       │
│ Error Recovery Agent (OpenAI GPT)      │
│ ↓                                       │
│ Monitoring Dashboard API                │
└─────────────────────────────────────────┘
```

## Features

### 1. **Centralized Logging**
- All errors logged to `logs/errors.jsonl`
- JSON format for easy parsing
- Timestamp, context, and traceback included

### 2. **AI Error Analysis**
- Automatic root cause analysis
- Severity classification (low/medium/high/critical)
- Fix suggestions with code examples
- Prevention strategies

### 3. **Error Monitoring Dashboard**
- Real-time error statistics
- Error breakdown by type
- AI agent health status
- Recent error history
- Auto-refresh every 10 seconds

### 4. **Frontend Error Reporting**
- Global error handler for uncaught exceptions
- Unhandled promise rejection tracking
- Automatic sending to backend
- Error backlog in case of offline

## API Endpoints

### Error Reporting
```
POST /api/monitoring/errors/report
Content-Type: application/json

{
  "error_type": "ValidationError",
  "message": "Invalid input",
  "context": { "field": "email" },
  "traceback": "...",
  "url": "http://localhost:3000/dashboard",
  "userAgent": "Mozilla/5.0..."
}

Response: { "status": "success", "message": "Error logged successfully" }
```

### Get Monitoring Dashboard
```
GET /api/monitoring/dashboard
Authorization: Bearer <token>

Response: {
  "total_recent_errors": 5,
  "error_counts": { "ValidationError": 3, "NetworkError": 2 },
  "ai_agent_healthy": true,
  "recent_errors": [...],
  "user": { "id": 1, "username": "john", "email": "john@example.com" }
}
```

### AI Error Analysis
```
POST /api/monitoring/errors/analyze
Authorization: Bearer <token>
Content-Type: application/json

{
  "error_type": "KeyError",
  "message": "'user_id' not found",
  "context": { "function": "get_user" },
  "traceback_str": "..."
}

Response: {
  "status": "success",
  "analysis": "Root cause analysis and fix suggestions...",
  "error_type": "KeyError",
  "timestamp": "2026-03-14T12:59:19.123Z"
}
```

### AI Fix Suggestion
```
POST /api/monitoring/errors/fix-suggestion
Authorization: Bearer <token>
Content-Type: application/json

{
  "error_type": "TypeError",
  "message": "unsupported operand type(s) for +: 'int' and 'str'",
  "previous_attempts": ["Added type() check", "Cast string to int"]
}

Response: {
  "status": "success",
  "fix": "Suggested code solution...",
  "error_type": "TypeError",
  "timestamp": "2026-03-14T12:59:19.123Z"
}
```

### AI Agent Health Check
```
GET /api/monitoring/health/ai-agent

Response: {
  "status": "healthy",
  "ai_available": true,
  "service": "error_recovery_agent"
}
```

## Usage

### 1. **Using the Monitoring Dashboard**

Navigate to: `http://localhost:3000/dashboard/monitoring`

The dashboard shows:
- Total errors count
- Error type breakdown
- AI agent status
- Recent errors with context
- Real-time auto-refresh

### 2. **Error Reporting from Frontend**

Errors are automatically caught and reported:

```typescript
// Automatic error handling
import { errorReporter } from '@/services/errorReporter'

// Manual error report
try {
  // Some operation
} catch (error) {
  await errorReporter.reportError(
    'CustomError',
    error.message,
    { operation: 'saveProject' },
    error.stack
  )
}
```

### 3. **Getting AI Analysis**

Via API:
```bash
curl -X POST http://localhost:8000/api/monitoring/errors/analyze \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "error_type": "ValueError",
    "message": "Invalid project ID",
    "context": {"project_id": "-1"}
  }'
```

## Configuration

### Environment Variables

```env
# Backend (.env)
OPENAI_API_KEY=sk-your-api-key-here
```

### AI Model Settings

Edit `backend/app/services/error_recovery.py`:

```python
class ErrorRecoveryAgent:
    def __init__(self):
        self.model = "gpt-3.5-turbo"  # Change model here
        self.temperature = 0.3         # Adjust creativity (0-1)
```

## Log Files

Errors are stored in:
- `backend/logs/app.log` - Full application logs
- `backend/logs/errors.jsonl` - Error records (one JSON per line)

### Example Error Record

```json
{
  "timestamp": "2026-03-14T12:59:19.123456",
  "type": "ValidationError",
  "message": "Invalid email format",
  "context": {
    "field": "email",
    "value": "invalid-email",
    "source": "user_input"
  },
  "traceback": "Traceback (most recent call last):\n  File \"app.py\", line 42..."
}
```

## Testing the Integration

### 1. Test Error Logging
```bash
# Backend logs automatically on errors
# Check logs/errors.jsonl
tail backend/logs/errors.jsonl
```

### 2. Test Error Reporting from Frontend
```bash
# Trigger an error in the web console
throw new Error('Test error')

# Check monitoring dashboard for the reported error
```

### 3. Test AI Analysis
```bash
curl -X POST http://localhost:8000/api/monitoring/errors/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"error_type":"Test","message":"This is a test error"}'
```

## Performance Considerations

- **Error Rate Limiting**: Not implemented (add if needed)
- **Backlog Size**: Frontend keeps max 50 errors in memory
- **Dashboard Refresh**: Every 10 seconds
- **AI Timeout**: OpenAI calls may take 2-5 seconds

## Security Notes

1. **API Protection**: All monitoring endpoints require authentication
2. **Rate Limiting**: Consider implementing for production
3. **Admin Only**: Restrict error viewing to admin users (implement in production)
4. **Sensitive Data**: Sanitize sensitive information before logging

## Future Enhancements

- [ ] WebSocket real-time error notifications
- [ ] Error pattern detection and alerts
- [ ] Automatic error fix implementation
- [ ] Team collaboration on error analysis
- [ ] Error prediction based on patterns
- [ ] Integration with external error tracking (Sentry)
- [ ] Machine learning for error classification
