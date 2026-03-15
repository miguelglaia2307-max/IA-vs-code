# API Quick Reference

Complete endpoint documentation with curl examples.

## Base URL
```
http://localhost:8000/api
```

## Interactive Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Projects

### List Projects
```bash
curl http://localhost:8000/api/projects
```

### Create Project
```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project",
    "description": "Project description"
  }'
```

### Get Project
```bash
curl http://localhost:8000/api/projects/1
```

### Update Project
```bash
curl -X PUT http://localhost:8000/api/projects/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "description": "Updated description"
  }'
```

### Delete Project
```bash
curl -X DELETE http://localhost:8000/api/projects/1
```

---

## Signatures

### List Signatures
```bash
curl "http://localhost:8000/api/signatures?project_id=1"
```

### Create Signature
```bash
curl -X POST http://localhost:8000/api/signatures \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "name": "Customer Support",
    "description": "Support ticket response",
    "input_fields": [
      {"name": "ticket", "type": "string"}
    ],
    "output_fields": [
      {"name": "response", "type": "string"}
    ]
  }'
```

### Get Signature
```bash
curl http://localhost:8000/api/signatures/1
```

### Update Signature
```bash
curl -X PUT http://localhost:8000/api/signatures/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name"
  }'
```

### Delete Signature
```bash
curl -X DELETE http://localhost:8000/api/signatures/1
```

---

## Datasets

### List Datasets
```bash
curl "http://localhost:8000/api/datasets?project_id=1"
```

### Create Dataset
```bash
curl -X POST http://localhost:8000/api/datasets \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "signature_id": 1,
    "name": "Support Examples",
    "examples": [
      {
        "input": "My order is late",
        "output": "I apologize for the delay. Let me look into this for you."
      },
      {
        "input": "Product is broken",
        "output": "I am sorry to hear that. We will replace it immediately."
      }
    ]
  }'
```

### Get Dataset
```bash
curl http://localhost:8000/api/datasets/1
```

### Update Dataset
```bash
curl -X PUT http://localhost:8000/api/datasets/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Dataset",
    "examples": [...]
  }'
```

### Delete Dataset
```bash
curl -X DELETE http://localhost:8000/api/datasets/1
```

---

## Metrics

### List Metrics
```bash
curl "http://localhost:8000/api/metrics?project_id=1"
```

### Create Metric
```bash
curl -X POST http://localhost:8000/api/metrics \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "signature_id": 1,
    "name": "Response Quality",
    "metric_type": "keyword_match",
    "config": {
      "keywords": ["apologize", "help", "solution"]
    }
  }'
```

**Metric Types:**
- `exact_match`: Check for exact output match
- `similarity`: String similarity using SequenceMatcher
- `keyword_match`: Check for keyword presence (recommended)
- `custom`: Custom scoring logic

### Get Metric
```bash
curl http://localhost:8000/api/metrics/1
```

### Update Metric
```bash
curl -X PUT http://localhost:8000/api/metrics/1 \
  -H "Content-Type: application/json" \
  -d '{
    "metric_type": "similarity"
  }'
```

### Delete Metric
```bash
curl -X DELETE http://localhost:8000/api/metrics/1
```

---

## Programs

### List Programs
```bash
curl "http://localhost:8000/api/programs?project_id=1"
```

### Create Program
```bash
curl -X POST http://localhost:8000/api/programs \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "signature_id": 1,
    "name": "Support Optimizer",
    "description": "Optimizes support response prompts",
    "code": "# Python code or template here"
  }'
```

### Get Program
```bash
curl http://localhost:8000/api/programs/1
```

### Update Program
```bash
curl -X PUT http://localhost:8000/api/programs/1 \
  -H "Content-Type: application/json" \
  -d '{
    "code": "# Updated code"
  }'
```

### Delete Program
```bash
curl -X DELETE http://localhost:8000/api/programs/1
```

---

## Optimization

### Start Optimization
```bash
curl -X POST http://localhost:8000/api/optimization/run \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "signature_id": 1,
    "metric_id": 1,
    "program_id": 1,
    "initial_prompt": "You are a helpful customer service agent",
    "dataset_id": 1,
    "num_iterations": 5,
    "variations_per_iteration": 3
  }'
```

**Response:**
```json
{
  "id": 1,
  "project_id": 1,
  "status": "running",
  "current_iteration": 0,
  "current_score": 0.0,
  "created_at": "2024-01-15T10:30:00"
}
```

### List Optimizations
```bash
curl "http://localhost:8000/api/optimization/runs?project_id=1"
```

### Get Optimization Status
```bash
curl http://localhost:8000/api/optimization/1
```

**Response:**
```json
{
  "id": 1,
  "project_id": 1,
  "signature_id": 1,
  "status": "running",
  "current_iteration": 2,
  "total_iterations": 5,
  "current_score": 0.654,
  "best_score": 0.654,
  "best_prompt": "You are a professional customer service expert...",
  "initial_prompt": "You are a helpful customer service agent",
  "variations_count": 6,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:35:45"
}
```

### Get Variations
```bash
curl "http://localhost:8000/api/optimization/1/variations"
```

**Response:**
```json
[
  {
    "id": 1,
    "prompt": "You are a helpful customer service agent",
    "score": 0.456,
    "iteration": 1,
    "is_best": false
  },
  {
    "id": 2,
    "prompt": "You are professional and empathetic...",
    "score": 0.654,
    "iteration": 2,
    "is_best": true
  }
]
```

### Stop Optimization
```bash
curl -X POST http://localhost:8000/api/optimization/1/stop
```

---

## Response Formats

### Success Response (200, 201)
```json
{
  "id": 1,
  "name": "Example",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### Error Response (400, 404, 500)
```json
{
  "detail": "Error message describing what went wrong"
}
```

### Status Codes
- `200 OK`: Request successful
- `201 Created`: Resource created
- `400 Bad Request`: Invalid input
- `404 Not Found`: Resource not found
- `500 Server Error`: Internal error

---

## Common Query Parameters

All list endpoints support filtering:

```bash
# Filter by project
curl "http://localhost:8000/api/signatures?project_id=1"

# Multiple filters work together
curl "http://localhost:8000/api/datasets?project_id=1"
```

---

## Authentication (Future)

Once authentication is implemented:

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Response
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}

# Use token in requests
curl http://localhost:8000/api/projects \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

---

## Workflow Example

### Complete Optimization Flow

```bash
# 1. Create project
PROJECT=$(curl -s -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{"name":"My Project","description":"Test"}' \
  | jq '.id')

# 2. Create signature
SIGNATURE=$(curl -s -X POST http://localhost:8000/api/signatures \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": '$PROJECT',
    "name": "Support",
    "input_fields": [{"name": "question", "type": "string"}],
    "output_fields": [{"name": "answer", "type": "string"}]
  }' | jq '.id')

# 3. Create dataset
DATASET=$(curl -s -X POST http://localhost:8000/api/datasets \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": '$PROJECT',
    "signature_id": '$SIGNATURE',
    "name": "Examples",
    "examples": [
      {"input": "How to reset?", "output": "Click forgot password"}
    ]
  }' | jq '.id')

# 4. Create metric
METRIC=$(curl -s -X POST http://localhost:8000/api/metrics \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": '$PROJECT',
    "signature_id": '$SIGNATURE',
    "name": "Quality",
    "metric_type": "keyword_match"
  }' | jq '.id')

# 5. Create program
PROGRAM=$(curl -s -X POST http://localhost:8000/api/programs \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": '$PROJECT',
    "signature_id": '$SIGNATURE',
    "name": "Optimizer",
    "code": ""
  }' | jq '.id')

# 6. Start optimization
RUN=$(curl -s -X POST http://localhost:8000/api/optimization/run \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": '$PROJECT',
    "signature_id": '$SIGNATURE',
    "metric_id": '$METRIC',
    "program_id": '$PROGRAM',
    "initial_prompt": "Help customers",
    "dataset_id": '$DATASET'
  }' | jq '.id')

# 7. Monitor progress
while true; do
  curl -s http://localhost:8000/api/optimization/$RUN | jq '.'
  sleep 5
done
```

---

## Environment Variables

### Backend
```bash
# .env file
DATABASE_URL=sqlite:///./data.db      # or postgresql://user:pass@host/db
OPENAI_API_KEY=sk-...                 # OpenAI API key
DEBUG=true                            # Enable debug mode
```

### Frontend
```bash
# .env.local file
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

---

## Testing with Tools

### Using REST Client Extension
Create `.vscode/requests.rest`:

```rest
### List Projects
GET http://localhost:8000/api/projects

### Create Project
POST http://localhost:8000/api/projects
Content-Type: application/json

{
  "name": "Test Project",
  "description": "A test project"
}

### Get Project
GET http://localhost:8000/api/projects/1

### Start Optimization
POST http://localhost:8000/api/optimization/run
Content-Type: application/json

{
  "project_id": 1,
  "signature_id": 1,
  "metric_id": 1,
  "program_id": 1,
  "initial_prompt": "Help customers",
  "dataset_id": 1
}
```

Then press "Send Request" next to each endpoint in VS Code.

### Using Postman
1. Create new Collection
2. Import endpoints from http://localhost:8000/openapi.json
3. Set environment variable: `api_url = http://localhost:8000/api`
4. Test each endpoint

---

## Rate Limiting (Future)

Once implemented, headers will include:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642252800
```

---

**Last Updated:** 2024-01-15
**API Version:** 1.0.0
