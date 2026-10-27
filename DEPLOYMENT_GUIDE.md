# 🚀 Render Deployment & GitHub Push Guide

This guide explains step-by-step how to initialize git, push this deployment repository to GitHub, and deploy it to **Render** for free with a single click.

---

## 📋 Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Step 1: Push This Folder to GitHub](#step-1-push-this-folder-to-github)
3. [Step 2: Deploy to Render](#step-2-deploy-to-render)
   - [Option A: Deploy with Docker (Recommended - 100% Free & Reliable)](#option-a-deploy-with-docker-recommended---easiest--100-free)
   - [Option B: Deploy via Render Blueprint (render.yaml)](#option-b-deploy-via-render-blueprint-renderyaml)
4. [Step 3: Configure Environment Variables on Render](#step-3-configure-environment-variables-on-render)
5. [Step 4: Verify Deployment & Login](#step-4-verify-deployment--login)
6. [Troubleshooting & FAQ](#troubleshooting--faq)

---

## 1. Prerequisites
- A **GitHub Account**: [github.com](https://github.com)
- A **Render Account**: [render.com](https://render.com) (Free tier supported)
- A **Groq API Key**: [console.groq.com/keys](https://console.groq.com/keys) (Free tier)
- Optional: A **GitHub Personal Access Token** to increase repository analysis API limits.

---

## Step 1: Push This Folder to GitHub

Open PowerShell or Terminal inside this directory (`github-analyzer-deployment`):

```powershell
# 1. Navigate to this deployment directory
cd "d:\Coding\rightcand-aug10\github-analyzer-deployment"

# 2. Initialize a new git repository
git init -b main

# 3. Add all files to staging
git add .

# 4. Create your initial commit
git commit -m "Initial commit: Production-ready RightCand & SCES platform for Render"

# 5. Create a new repository on GitHub (via browser):
#    Go to https://github.com/new and create a repository (e.g., 'rightcand-platform').
#    DO NOT initialize with README, .gitignore, or license.

# 6. Link to your GitHub repository and push (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

## Step 2: Deploy to Render

### Option A: Deploy with Docker (Recommended - Easiest & 100% Free)
Docker automatically handles Node.js frontend builds and Python ASGI dependencies with zero version conflicts.

1. Go to your [Render Dashboard](https://dashboard.render.com).
2. Click **New +** in the top right corner and select **Web Service**.
3. Select **Build and deploy from a Git repository** and click **Next**.
4. Connect your GitHub account and select your repository (`rightcand-platform`).
5. Configure the service settings:
   - **Name**: `rightcand-fullstack` (or your preferred name)
   - **Region**: Choose the closest region (e.g., `Oregon (US West)` or `Frankfurt`)
   - **Branch**: `main`
   - **Root Directory**: Leave blank (uses repository root)
   - **Runtime**: Select **Docker**
   - **Instance Type**: Select **Free** ($0/month)
6. Scroll down to **Environment Variables** (see [Step 3](#step-3-configure-environment-variables-on-render)).
7. Click **Create Web Service**.

> **Note**: The initial Docker build takes ~2 to 4 minutes to compile the Vite frontends and install Python dependencies. Once completed, your app will be live at `https://your-app-name.onrender.com`!

---

### Option B: Deploy via Render Blueprint (render.yaml)
1. Go to your [Render Dashboard](https://dashboard.render.com).
2. Click **New +** and select **Blueprint**.
3. Connect your repository.
4. Render will automatically detect `render.yaml` and configure the service for you!
5. Add your `GROQ_API_KEY` when prompted and click **Apply**.

---

## Step 3: Configure Environment Variables on Render

In your Render Web Service dashboard, go to the **Environment** tab and add the following keys:

| Variable | Value | Description | Required? |
| :--- | :--- | :--- | :---: |
| `GROQ_API_KEY` | `gsk_...` | Your Groq API Key | **Yes** |
| `GITHUB_TOKEN` | `ghp_...` | GitHub Personal Access Token | Optional (Recommended) |
| `SECRET_KEY` | *(any random string)* | JWT Signing Secret | Optional |
| `ALLOWED_ORIGINS` | `*` | Allowed CORS origins | Optional (Default: `*`) |
| `PORT` | `10000` | Port Render listens on | Managed by Render |

---

## Step 4: Verify Deployment & Login

Once Render status shows **Live**:

### 🌐 Accessing the Portals:
- **Main Portal (Talent Vellocity SCES)**:  
  `https://your-service.onrender.com/`
- **AI Interview Assistant**:  
  `https://your-service.onrender.com/interview` (or click **🎯 AI Interview Prep** on your profile navbar)
- **Placement Readiness Verdict Dashboard**:  
  `https://your-service.onrender.com/verdict`
- **Interactive Swagger API Documentation**:  
  `https://your-service.onrender.com/docs`
- **Health Check Endpoint**:  
  `https://your-service.onrender.com/health`

### 🔑 Pre-Seeded Default Accounts:

#### 1. Admin Account:
- **Username**: `admin`
- **Password**: `admin123`
- **Access**: Full admin dashboard, percentile tuner, custom weight sliders, student explainability drawer.

#### 2. Sample Student Profiles (Pre-loaded with stats and projects):
- `raghul`
- `antony`
- `moneshwar`
- `madan`
- `sharan`

---

## Troubleshooting & FAQ

### Q: Why deploy as a single unified service instead of 5 separate services?
Render's Free Tier includes **750 free instance hours per month**. If you run 3 or 5 separate web services, you would consume your monthly free quota in under 10 days! The unified server combines all services into **1 single container**, meaning you stay **100% within the free tier forever**, with zero CORS issues and no inter-service networking failures.

### Q: Does the SQLite database persist on Render free tier?
On Render's Free tier, the filesystem is ephemeral (it resets on restarts/deploys). The database comes **pre-seeded** with 9 user accounts and the default admin (`admin` / `admin123`). If you need permanent data persistence across restarts on Render:
1. You can attach a Render Disk (paid tier), or
2. Plug in an external PostgreSQL database by setting the `DATABASE_URL` environment variable (e.g. Supabase, Neon, or Render PostgreSQL).

### Q: How do I test the unified server locally before deploying?
Run the unified server launcher script:
```powershell
.\start_unified_local.ps1
```
Then visit `http://localhost:8000` in your browser.
