# RightCand & SCES: Centralized Evaluation and Agentic Interview Assistant

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

This repository contains the complete production-ready **RightCand & Student Centralized Evaluation System (SCES)** platform, featuring a deterministic GitHub Repository Analyzer engine, an embedded sequential Multi-Agent AI Interview Preparation Assistant, and a Placement Readiness Verdict Agent.

---

## 🚀 Quick Deployment to Render

To deploy this repository to Render in under 5 minutes, follow our step-by-step [Deployment Guide](DEPLOYMENT_GUIDE.md).

### Quick Steps:
1. Push this folder to your GitHub:
   ```bash
   git init -b main
   git add .
   git commit -m "Deploy RightCand ecosystem"
   git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
   git push -u origin main
   ```
2. In Render, select **New Web Service** → Connect your repository → Select **Docker** environment.
3. Add `GROQ_API_KEY` under Environment Variables.
4. Click **Deploy**!

---

## 📂 Project Architecture

```
github-analyzer-deployment/
├── Dockerfile                                          # Multi-stage Docker build (Vite + Python 3.11)
├── render.yaml                                         # Render Blueprint infrastructure specification
├── unified_server.py                                   # Master ASGI production server hosting all portals & APIs
├── requirements.txt                                    # Clean, lightweight production Python dependencies
├── DEPLOYMENT_GUIDE.md                                 # Complete Render & GitHub walkthrough
│
├── Talent Vellocity/sces/                              # Main Student Evaluation Portal (SCES)
│   ├── backend/                                        # FastAPI Backend API + SQLite ORM
│   │   ├── app/models/models.py                        # Database Schemas
│   │   ├── app/routes/                                 # Auth, profile, admin, and project routes
│   │   └── sces.db                                     # Pre-seeded database (admin & 9 students)
│   └── frontend/                                       # React 18 + Vite Glassmorphic Dashboard
│
├── github-analyzer-agent/                              # GitHub Analyzer Pipeline Engine
│   └── backend/                                        # Deterministic extractor & LLM classifier (Groq)
│       ├── github_client.py                            # GitHub REST API client
│       ├── extractors.py                               # Dependency manifests & complexity parser
│       └── llm_agent.py                                # Grounded taxonomy classifier
│
├── final-capstone-project-agentic-ai-interview.../     # AI Interview Preparation Assistant
│   ├── agents/                                         # 7 Sequential Multi-Agent decision pipeline
│   ├── utils/                                          # PDF extraction utilities
│   ├── api.py                                          # FastAPI interview coordinator
│   └── frontend/                                       # React 19 + Vite + Tailwind CSS Interview UI
│
└── readiness-verdict-agent/                            # Placement Readiness Verdict Agent
    ├── app.py                                          # FastAPI service
    ├── verdict_agent.py                                # Heuristic readiness evaluation engine
    ├── documents/                                      # Sample benchmark student profiles
    └── static/                                         # Standalone analytics dashboard UI
```

---

## 🤖 AI Agents Inventory

The platform is powered by **9 autonomous AI Agents**:

### 🔍 GitHub Repo Analyzer Pipeline (`github-analyzer-agent/`)
1. **Grounded Taxonomy Classifier Agent**: Classifies a student's project codebase into target domains out of a fixed taxonomy of 15 domains, strictly grounded with evidence citations.

### 🎙️ AI Interview Preparation Assistant (`final-capstone-project.../`)
2. **Resume Agent**: Extracts candidate profile details, technical credentials, and stated technologies from CVs.
3. **JD Agent**: Analyzes required skill stacks and primary expectations from target Job Descriptions.
4. **Gap Agent**: Computes missing capabilities and matches student profiles against job requirements.
5. **Planner Agent**: Schedules a customized 10-slot questionnaire roadmap tailored to the student's real projects and gaps.
6. **Question Generator Agent**: Drafts contextual technical interview questions grounded in candidate repositories.
7. **Interview Agent**: Manages the conversational progression through the planned questionnaire roadmap.
8. **Evaluation Agent**: Grades candidate answers for coding depth, logical precision, and clarity.
9. **Report Agent**: Compiles the final candidate scorecard detailing overall candidate fit and readiness.

---

## 💻 Local Testing & Development

You can run the project locally using either mode:

### Mode 1: Production Simulator (Unified Single Port)
```powershell
.\start_unified_local.ps1
```
All endpoints and UIs will be accessible at `http://localhost:8000`.

### Mode 2: Multi-Process Development (Separate Ports)
```powershell
.\start_local.ps1
```
- Talent Vellocity Portal: `http://localhost:5173`
- AI Interview Assistant: `http://localhost:5174`
- Readiness Verdict Agent: `http://localhost:8002`
- Talent Vellocity API: `http://localhost:8000/docs`
- Capstone Interview API: `http://localhost:8090/docs`

---

## 🔑 Default Credentials

- **Admin Login**: `admin` / `admin123`
- **Sample Students**: `raghul`, `antony`, `moneshwar`, `madan`, `sharan`
