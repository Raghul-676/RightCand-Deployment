# ==============================================================================
# RightCand Unified Production Server Local Launcher
# Simulates the Render production environment on your local machine
# ==============================================================================

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " RightCand Fullstack Unified Server (Render Simulator)" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Port: 8000 (All services, APIs & UIs running on one port)" -ForegroundColor Yellow
Write-Host "Main Portal:           http://localhost:8000" -ForegroundColor Green
Write-Host "AI Interview Prep:     http://localhost:8000/interview" -ForegroundColor Green
Write-Host "Readiness Verdict:     http://localhost:8000/verdict" -ForegroundColor Green
Write-Host "API Documentation:     http://localhost:8000/docs" -ForegroundColor Green
Write-Host "Health Check:          http://localhost:8000/health" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to terminate the server." -ForegroundColor Gray
Write-Host ""

Set-Location $ScriptDir
python unified_server.py
