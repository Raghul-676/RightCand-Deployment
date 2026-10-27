#!/usr/bin/env bash
# ==============================================================================
# Render Native Build Script (for Python Web Service on Render)
# ==============================================================================
set -o errexit

echo "📦 Upgrading pip and installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎨 Building Talent Vellocity (SCES) Frontend..."
cd "Talent Vellocity/sces/frontend"
npm install
npm run build
cd ../../..

echo "🎙️ Building Capstone AI Interview Assistant Frontend..."
cd "final-capstone-project-agentic-ai-interview-preparation-assistant/frontend"
npm install
VITE_BASE_PATH=/interview/ npm run build
cd ../..

echo "✅ Build completed successfully! Ready for launch."
