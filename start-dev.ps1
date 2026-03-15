# Script para iniciar Frontend e Backend simultaneamente

Write-Host "Iniciando Prompt Optimization Platform..." -ForegroundColor Cyan
Write-Host ""

# Verificar se as pastas existem
if (-not (Test-Path ".\backend")) {
    Write-Host "ERRO: Pasta 'backend' nao encontrada!" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path ".\frontend")) {
    Write-Host "ERRO: Pasta 'frontend' nao encontrada!" -ForegroundColor Red
    exit 1
}

# Iniciar Backend
Write-Host "Iniciando Backend (FastAPI)..." -ForegroundColor Green
Write-Host "   Esperando em http://localhost:8000" -ForegroundColor Gray

$backendCmd = "cd backend; python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $backendCmd

# Esperar um pouco para o backend iniciar
Start-Sleep -Seconds 3

# Iniciar Frontend
Write-Host "Iniciando Frontend (Next.js)..." -ForegroundColor Blue
Write-Host "   Esperando em http://localhost:3000" -ForegroundColor Gray

$frontendCmd = "cd frontend; npm run dev"
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", $frontendCmd

Write-Host ""
Write-Host "Ambos os servidores foram iniciados!" -ForegroundColor Green
Write-Host ""
Write-Host "Acesse:" -ForegroundColor Yellow
Write-Host "   Landing Page: http://localhost:3000" -ForegroundColor Cyan
Write-Host "   Dashboard:    http://localhost:3000/dashboard" -ForegroundColor Cyan
Write-Host "   API Docs:     http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

