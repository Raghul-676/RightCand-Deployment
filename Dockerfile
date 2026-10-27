# ==============================================================================
# Multi-Stage Production Dockerfile for RightCand Ecosystem (Render Ready)
# ==============================================================================

# ------------------------------------------------------------------------------
# Stage 1: Build React Frontends with Node.js
# ------------------------------------------------------------------------------
FROM node:20-alpine AS frontend-builder
WORKDIR /build

# 1. Build Talent Vellocity (SCES) Frontend
COPY ["Talent Vellocity/sces/frontend/package*.json", "./sces-frontend/"]
RUN cd sces-frontend && npm install

COPY ["Talent Vellocity/sces/frontend", "./sces-frontend"]
RUN cd sces-frontend && npm run build

# 2. Build Capstone AI Interview Assistant Frontend
COPY ["final-capstone-project-agentic-ai-interview-preparation-assistant/frontend/package*.json", "./capstone-frontend/"]
RUN cd capstone-frontend && npm install

COPY ["final-capstone-project-agentic-ai-interview-preparation-assistant/frontend", "./capstone-frontend"]
# Set VITE_BASE_PATH to /interview/ so Vite resolves assets at /interview/
ENV VITE_BASE_PATH=/interview/
RUN cd capstone-frontend && npm run build


# ------------------------------------------------------------------------------
# Stage 2: Python 3.11 Runtime & ASGI Server
# ------------------------------------------------------------------------------
FROM python:3.11-slim AS runner

WORKDIR /app

# Prevent Python from writing pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Install minimal OS dependencies for gitpython and sqlite
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all application code
COPY . .

# Copy built frontend dist folders from Stage 1 into proper locations
# COPY --from=frontend-builder /build/sces-frontend/dist ./Talent\ Vellocity/sces/frontend/dist
COPY --from=frontend-builder ["/build/sces-frontend/dist", "./Talent Vellocity/sces/frontend/dist"]
COPY --from=frontend-builder /build/capstone-frontend/dist ./final-capstone-project-agentic-ai-interview-preparation-assistant/frontend/dist

# Expose default Render port
EXPOSE 10000

# Run unified server on dynamic Render PORT
CMD ["sh", "-c", "exec uvicorn unified_server:app --host 0.0.0.0 --port ${PORT:-10000}"]
