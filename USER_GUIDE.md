# User Guide - Prompt Optimization Platform

## 🎯 Overview

The Prompt Optimization Platform helps you automatically improve your prompts. Instead of manually tweaking, the system:
1. Takes your initial prompt
2. Generates 15 variations (3 per iteration × 5 iterations)
3. Evaluates each against your test examples
4. Keeps the best performer

## 🚀 Getting Started

### Step 1: Start Both Servers

**Terminal 1 - Backend**
```bash
cd backend
pip install -r requirements.txt
python seed.py
python run.py
```

**Terminal 2 - Frontend**
```bash
cd frontend
npm install
npm run dev
```

### Step 2: Open Dashboard
Go to: `http://localhost:3000/dashboard`

You should see a test project: **"Customer Service Optimization"**

## 📖 User Workflow

### Option A: Using Test Project (Fast - 2 minutes)

1. **View Dashboard**
   - URL: `http://localhost:3000/dashboard`
   - See "Customer Service Optimization" project
   - Click **"Open"**

2. **Start Optimization**
   - Click **▶ "Iniciar Nova Otimização"** button
   - Pop-up asks for initial prompt
   - Enter example: `You are a helpful customer service agent`
   - Click OK

3. **Watch Progress**
   - Click the optimization link
   - See iterations, variations, and scores updating
   - Watch best prompt improve with each iteration

4. **View Results**
   - Scroll down to see all variations
   - Check the "Melhor Prompt Encontrado" section
   - Copy optimized prompt for use

### Option B: Create Your Own Project (15 minutes)

#### 1. Create a Project
**Dashboard** → Click **"+ Novo Projeto"**
- Name: "My Optimization"
- Description: "Optimize my custom prompts"
- Click **"Criar"**

#### 2. Create a Signature (Input/Output Contract)
**Open Project** → **"Configuração" tab** → Need Signature

Using API (or use seed data):
```bash
curl -X POST http://localhost:8000/api/signatures/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": YOUR_PROJECT_ID,
    "name": "Translation",
    "description": "Translate English to Spanish",
    "input_fields": [{"name": "text", "type": "string"}],
    "output_fields": [{"name": "translation", "type": "string"}]
  }'
```

#### 3. Add Dataset (Examples)
**Configure** → Need Dataset

```bash
curl -X POST http://localhost:8000/api/datasets/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "signature_id": 1,
    "name": "Translation Examples",
    "examples": [
      {"input": "Hello", "output": "Hola"},
      {"input": "Good morning", "output": "Buenos días"}
    ]
  }'
```

#### 4. Define Metric (How to Score)
**Configure** → Need Metric

```bash
curl -X POST http://localhost:8000/api/metrics/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "signature_id": 1,
    "name": "Translation Quality",
    "metric_type": "keyword_match"
  }'
```

#### 5. Create Program (Executor)
**Configure** → Need Program

```bash
curl -X POST http://localhost:8000/api/programs/ \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "signature_id": 1,
    "name": "Translation Runner",
    "description": "Runs translation optimization",
    "code": "# Placeholder"
  }'
```

#### 6. Start Optimization
**Project Dashboard** → **▶ "Iniciar Nova Otimização"**
- Enter example prompt: `Translate the following text to Spanish:`
- Watch the magic happen!

## 🔍 Understanding the Dashboard

### Projects Page
```
┌─ Projects Dashboard ─────────────────────────┐
│                                               │
│  + Novo Projeto                               │
│                                               │
│  ┌── Project Card 1 ──────────────────────┐  │
│  │ Customer Service Optimization           │  │
│  │ Optimize customer support prompts       │  │
│  │                                          │  │
│  │  [Abrir]              [Deletar]         │  │
│  └──────────────────────────────────────────┘  │
│                                                │
│  ┌── Project Card 2 ──────────────────────┐  │
│  │ My Custom Project                       │  │
│  │ Custom optimization task                │  │
│  │                                          │  │
│  │  [Abrir]              [Deletar]         │  │
│  └──────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

### Project Detail Page
```
┌─ Project Detail ─────────────────────────────┐
│ ← Voltar                                      │
│                                               │
│ Customer Service Optimization                 │
│ [Configuração]  [Otimizações (3)]             │
│                                               │
│ ▶ Iniciar Nova Otimização                     │
│                                               │
│ Configuração Tab:                             │
│ ┌──────────────┬──────────────┐             │
│ │ Signatures   │ Datasets     │             │
│ │ (1)          │ (1)          │             │
│ ├──────────────┼──────────────┤             │
│ │ Metrics      │ Programs     │             │
│ │ (1)          │ (1)          │             │
│ └──────────────┴──────────────┘             │
└──────────────────────────────────────────────┘
```

### Optimization Monitor Page
```
┌─ Optimization #1 ────────────────────────────┐
│ ← Voltar para Projeto                         │
│                                               │
│ ┌─ Status ─┬─ Score ─┬─ Iterations ─┬─ Variations ┐
│ │ running  │ 65.4%   │ 2/5          │ 6          │
│ └──────────┴─────────┴──────────────┴─────────────┘
│                                               │
│ Prompt Inicial:                               │
│ ┌────────────────────────────────────────────┐
│ │ You are a helpful customer service agent   │
│ └────────────────────────────────────────────┘
│                                               │
│ Melhor Prompt Encontrado:                     │
│ ┌────────────────────────────────────────────┐
│ │ You are a professional, empathetic...      │
│ └────────────────────────────────────────────┘
│                                               │
│ Progresso por Iteração:                       │
│ ┌─ Iteração 1 ─────────────────── 58.3% ───┐│
│ │ Variação 1: 45.2%                        ││
│ │ Variação 2: 52.1%                        ││
│ │ Variação 3: 58.3% ← Best                 ││
│ └─────────────────────────────────────────────┘│
│ ┌─ Iteração 2 ─────────────────── 65.4% ───┐│
│ │ Variação 1: 60.1%                        ││
│ │ Variação 2: 65.4% ← Best                 ││
│ │ Variação 3: 63.2%                        ││
│ └─────────────────────────────────────────────┘│
└──────────────────────────────────────────────────┘
```

## 📊 Example Optimization Results

**Initial Prompt:**
```
You are a helpful customer service agent
```

**After Optimization (Iteration 1):**
```
You are a patient, professional customer service representative who prioritizes 
customer satisfaction and provides clear, helpful solutions
```

**After Optimization (Iteration 2):**
```
You are an empathetic, solution-focused customer service professional. 
Your goal is to resolve customer issues quickly while maintaining a warm, 
understanding tone.
```

**After Optimization (Iteration 3):**
```
You are a customer-centric professional with expertise in conflict resolution. 
Listen carefully, empathize sincerely, and provide practical solutions. 
Maintain a warm, helpful tone throughout.
```

## 💡 Tips for Best Results

### Good Test Data
- Include diverse examples
- Cover edge cases
- Use realistic scenarios
- Have 5-10 examples minimum

```json
"examples": [
  {"input": "Order late", "output": "Sincerely apologize..."},
  {"input": "Product broken", "output": "We'll replace..."},
  {"input": "Password reset", "output": "Click Forgot Password..."}
]
```

### Good Metrics
- Choose metric type that matches your use case:
  - **keyword_match**: For checking presence of key concepts
  - **similarity**: For similar-sounding responses
  - **exact_match**: For strict validation
  - **custom**: For complex requirements

### Good Initial Prompts
- Be specific: ✅ "Respond as a patient doctor" vs ❌ "Respond"
- Add constraints: ✅ "Use technical language" vs ❌ "Respond"
- Provide context: ✅ "Customer is angry" vs ❌ "Respond"

## 🔄 Optimization Process

```
START
  ↓
[Initial Prompt] → "You are helpful..."
  ↓
ITERATION 1:
  ├─→ Generate 3 variations
  ├─→ Evaluate against dataset
  ├─→ Keep best (58%)
  ↓
ITERATION 2:
  ├─→ Generate 3 more variations from best
  ├─→ Evaluate against dataset
  ├─→ Keep best (65%)
  ↓
ITERATION 3:
  ├─→ Generate 3 more variations
  ├─→ Evaluate
  ├─→ Keep best (72%)
  ↓
[Continue... Iterations 4 & 5]
  ↓
RESULT:
  ★ Best Prompt (Final Score: 75%)
END
```

## 🛠️ Troubleshooting

### "Cannot start optimization - missing requirements"
- Create all 4 components first (Signature, Dataset, Metric, Program)
- Check project detail page to see what's missing

### "Optimization stuck on 'running'"
- Optimizations take ~1-2 minutes per iteration
- Auto-refresh happens every 3 seconds
- Check backend logs for errors

### "Cannot upload dataset"
- Examples must have "input" and "output" keys
- Check JSON formatting is valid

### "API connection error"
- Verify backend is running: `http://localhost:8000/docs`
- Check NEXT_PUBLIC_API_URL in frontend .env.local
- Ensure ports 3000 and 8000 are free

## 📚 Learn More

- **Full Setup**: See [GETTING_STARTED.md](./GETTING_STARTED.md)
- **API Docs**: `http://localhost:8000/docs` (interactive Swagger)
- **Development**: See [DEVELOPMENT.md](./DEVELOPMENT.md)
- **Architecture**: See [ARCHITECTURE.md](./ARCHITECTURE.md)

## 🎓 Example Use Cases

### 1. Customer Support
- Optimize responses to customer queries
- Improve empathy and clarity
- Maintain professional tone

### 2. Content Generation
- Refine blog post prompts
- Improve SEO optimization
- Maintain brand voice

### 3. Code Comments
- Better documentation prompts
- Improve clarity
- Meet style guidelines

### 4. Translations
- Improve translation accuracy
- Maintain tone consistency
- Handle cultural nuances

### 5. Data Extraction
- Refine extraction prompts
- Improve field accuracy
- Handle edge cases

## 🎯 Next Steps

1. ✅ Start both servers (10 seconds)
2. ✅ Open dashboard (1 second)
3. ✅ Run test optimization (2 minutes)
4. ✅ Create your own project (10 minutes)
5. ✅ Integrate optimized prompts into your app (varies)

**Total time to first working optimization: ~5 minutes!**

---

**Happy Optimizing! 🚀**
