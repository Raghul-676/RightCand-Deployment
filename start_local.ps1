# ==============================================================================
# RightCand Local Multi-Process Development Launcher
# Starts individual backend & frontend services on dedicated ports
# ==============================================================================

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Talent Vellocity Backend (Port 8000)
$BackendCwd = Join-Path $ScriptDir "Talent Vellocity\sces\backend"
Start-Process powershell -ArgumentList "-Command", "cd '$BackendCwd'; uvicorn app.main:app --port 8000 --reload" -WindowStyle Hidden

# 2. Talent Vellocity Frontend (Port 5173)
$FrontendCwd = Join-Path $ScriptDir "Talent Vellocity\sces\frontend"
Start-Process powershell -ArgumentList "-Command", "cd '$FrontendCwd'; npm run dev" -WindowStyle Hidden

# 3. Capstone Interview Prep Backend (Port 8090)
$CapstoneBackendCwd = Join-Path $ScriptDir "final-capstone-project-agentic-ai-interview-preparation-assistant"
Start-Process powershell -ArgumentList "-Command", "cd '$CapstoneBackendCwd'; uvicorn api:app --port 8090 --reload"

# 4. Capstone Interview Prep Frontend (Port 5174)
$CapstoneFrontendCwd = Join-Path $ScriptDir "final-capstone-project-agentic-ai-interview-preparation-assistant\frontend"
Start-Process powershell -ArgumentList "-Command", "cd '$CapstoneFrontendCwd'; npm run dev" -WindowStyle Hidden

# 5. Placement Readiness Verdict Agent (Port 8002)
$VerdictCwd = Join-Path $ScriptDir "readiness-verdict-agent"
Start-Process powershell -ArgumentList "-Command", "cd '$VerdictCwd'; uvicorn app:app --port 8002 --reload" -WindowStyle Hidden

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host " All local development servers are now active:" -ForegroundColor Green
Write-Host "   - Talent Vellocity Portal:   http://localhost:5173" -ForegroundColor Yellow
Write-Host "   - AI Interview Assistant:    http://localhost:5174" -ForegroundColor Yellow
Write-Host "   - Readiness Verdict Agent:   http://localhost:8002" -ForegroundColor Yellow
Write-Host "   - Talent Vellocity API:      http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "   - Capstone Interview API:    http://localhost:8090/docs" -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Green
Write-Host ""
Read-Host "Press [ENTER] to stop all servers and free up ports (8000, 8090, 8002, 5173, 5174)"

Write-Host "Terminating application processes..." -ForegroundColor Red
$Ports = @(8000, 8090, 8002, 5173, 5174)
foreach ($Port in $Ports) {
    $Conns = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    foreach ($Conn in $Conns) {
        if ($Conn.OwningProcess) {
            Stop-Process -Id $Conn.OwningProcess -Force -ErrorAction SilentlyContinue
        }
    }
}
Write-Host "All local servers stopped cleanly. Port release complete!" -ForegroundColor Green
