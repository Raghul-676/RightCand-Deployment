"""
RightCand Unified Production Server (Render Ready)
==================================================
Runs the complete Student Centralized Evaluation System (Talent Vellocity),
Multi-Agent AI Interview Assistant (Capstone), and Readiness Verdict Agent
under a single unified ASGI application on a single port.
"""

import os
import sys
import importlib.util
from pathlib import Path
from dotenv import load_dotenv

# 1. Resolve workspace paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SCES_BACKEND_DIR = os.path.join(ROOT_DIR, "Talent Vellocity", "sces", "backend")
SCES_FRONTEND_DIST = os.path.join(ROOT_DIR, "Talent Vellocity", "sces", "frontend", "dist")
AGENT_BACKEND_DIR = os.path.join(ROOT_DIR, "github-analyzer-agent", "backend")
CAPSTONE_DIR = os.path.join(ROOT_DIR, "final-capstone-project-agentic-ai-interview-preparation-assistant")
CAPSTONE_FRONTEND_DIST = os.path.join(CAPSTONE_DIR, "frontend", "dist")
VERDICT_DIR = os.path.join(ROOT_DIR, "readiness-verdict-agent")

# 2. Add search paths to sys.path with SCES_BACKEND_DIR taking precedence for 'app' package
for path in [AGENT_BACKEND_DIR, ROOT_DIR]:
    if os.path.exists(path) and path not in sys.path:
        sys.path.append(path)

if SCES_BACKEND_DIR not in sys.path:
    sys.path.insert(0, SCES_BACKEND_DIR)

# 3. Load Environment Variables (.env)
load_dotenv(os.path.join(ROOT_DIR, ".env"))
if os.path.exists(os.path.join(SCES_BACKEND_DIR, ".env")):
    load_dotenv(os.path.join(SCES_BACKEND_DIR, ".env"))
if os.path.exists(os.path.join(AGENT_BACKEND_DIR, ".env")):
    load_dotenv(os.path.join(AGENT_BACKEND_DIR, ".env"))
if os.path.exists(os.path.join(CAPSTONE_DIR, ".env")):
    load_dotenv(os.path.join(CAPSTONE_DIR, ".env"))

# 4. Import FastAPI & Dependencies
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# 5. Database Setup (Talent Vellocity)
from app.database import engine, SessionLocal
from app.models.models import Base, User
from app.services.auth_service import hash_password
from app.routes import auth, profile, admin, projects

Base.metadata.create_all(bind=engine)

def seed_admin():
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.username == "admin").first():
            db.add(User(
                username="admin",
                email="admin@codetracker.local",
                hashed_password=hash_password("admin123"),
                role="admin",
                profile_setup_done=1,
            ))
            db.commit()
    finally:
        db.close()

seed_admin()

# 6. Load Capstone API module
if CAPSTONE_DIR not in sys.path:
    sys.path.insert(0, CAPSTONE_DIR)
capstone_api_file = os.path.join(CAPSTONE_DIR, "api.py")
capstone_spec = importlib.util.spec_from_file_location("capstone_api_module", capstone_api_file)
capstone_mod = importlib.util.module_from_spec(capstone_spec)
capstone_spec.loader.exec_module(capstone_mod)

# 7. Load Verdict Agent module
if VERDICT_DIR not in sys.path:
    sys.path.insert(0, VERDICT_DIR)
verdict_app_file = os.path.join(VERDICT_DIR, "app.py")
verdict_spec = importlib.util.spec_from_file_location("verdict_api_module", verdict_app_file)
verdict_mod = importlib.util.module_from_spec(verdict_spec)
verdict_spec.loader.exec_module(verdict_mod)

# 8. Create Unified Master App
app = FastAPI(
    title="RightCand - Centralized Evaluation & AI Interview Assistant",
    description="Unified API & UI portal for SCES, Multi-Agent Interview Assistant, and Placement Verdict.",
    version="3.0.0"
)

# 9. Configure CORS
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "").strip()
if allowed_origins_env and allowed_origins_env != "*":
    origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]
    allow_credentials = True
else:
    origins = ["*"]
    allow_credentials = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 10. Health Check Endpoints
@app.get("/health")
@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "service": "RightCand & SCES Ecosystem",
        "components": {
            "talent_vellocity": "online",
            "interview_prep_assistant": "online",
            "readiness_verdict_agent": "online",
            "github_analyzer_agent": "online"
        }
    }

# 11. Register Talent Vellocity Routes
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(admin.router)
app.include_router(projects.router)

# 12. Register Capstone AI Interview Routes (both direct & prefixed)
for route in capstone_mod.app.routes:
    if route.path not in ["/openapi.json", "/docs", "/redoc", "/"]:
        app.routes.append(route)

app.mount("/api/interview", capstone_mod.app)

# 13. Register Verdict Agent Routes
for route in verdict_mod.app.routes:
    if route.path not in ["/openapi.json", "/docs", "/redoc", "/"]:
        app.routes.append(route)

# Verdict Agent Dashboard HTML
@app.get("/verdict", response_class=HTMLResponse)
async def serve_verdict_dashboard():
    index_file = os.path.join(VERDICT_DIR, "static", "index.html")
    if os.path.exists(index_file):
        with open(index_file, "r", encoding="utf-8") as f:
            return f.read()
    raise HTTPException(status_code=404, detail="Verdict Agent dashboard HTML not found.")

# 14. Static Frontends Serving (Single-Page App routing)

# Capstone Frontend (mounted at /interview)
if os.path.exists(CAPSTONE_FRONTEND_DIST):
    app.mount("/interview/assets", StaticFiles(directory=os.path.join(CAPSTONE_FRONTEND_DIST, "assets")), name="interview_assets")
    
    @app.get("/interview/{full_path:path}")
    async def serve_capstone_spa(full_path: str):
        file_path = os.path.join(CAPSTONE_FRONTEND_DIST, full_path)
        if full_path and os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(CAPSTONE_FRONTEND_DIST, "index.html"))

    @app.get("/interview")
    async def serve_capstone_root():
        return FileResponse(os.path.join(CAPSTONE_FRONTEND_DIST, "index.html"))

# Talent Vellocity Frontend (mounted at root /)
if os.path.exists(SCES_FRONTEND_DIST):
    # Mount assets folder
    assets_dir = os.path.join(SCES_FRONTEND_DIST, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="sces_assets")

    # SPA catch-all route for Talent Vellocity
    @app.get("/{full_path:path}")
    async def serve_sces_spa(full_path: str):
        # Don't intercept API or doc routes
        if full_path.startswith("api/") or full_path in ["health", "docs", "redoc", "openapi.json", "verdict"]:
            raise HTTPException(status_code=404, detail="API route not found.")
        file_path = os.path.join(SCES_FRONTEND_DIST, full_path)
        if full_path and os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        index_html = os.path.join(SCES_FRONTEND_DIST, "index.html")
        if os.path.exists(index_html):
            return FileResponse(index_html)
        raise HTTPException(status_code=404, detail="Frontend file not found.")

else:
    @app.get("/")
    def index():
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>RightCand & SCES - Backend Active</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
                .card { background: #1e293b; padding: 2.5rem; border-radius: 1rem; border: 1px solid #334155; max-width: 600px; text-align: center; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5); }
                h1 { color: #38bdf8; margin-top: 0; font-size: 1.8rem; }
                p { color: #94a3b8; line-height: 1.6; }
                .badge { display: inline-block; background: #0284c7; color: white; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; margin-bottom: 1rem; }
                .links { margin-top: 1.5rem; display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap; }
                a { color: #38bdf8; text-decoration: none; background: #334155; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.9rem; transition: all 0.2s; }
                a:hover { background: #0284c7; color: white; }
            </style>
        </head>
        <body>
            <div class="card">
                <span class="badge">API ACTIVE</span>
                <h1>RightCand & SCES Backend Server</h1>
                <p>The backend services and AI agents are running successfully. Frontends can either be built into <code>dist/</code> folders or run using their Vite development servers.</p>
                <div class="links">
                    <a href="/docs" target="_blank">Swagger API Docs</a>
                    <a href="/health" target="_blank">Health Check</a>
                    <a href="/verdict" target="_blank">Readiness Verdict Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        """)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Starting RightCand Unified Server on port {port}...")
    uvicorn.run("unified_server:app", host="0.0.0.0", port=port, reload=False)
