#!/bin/bash
set -e

cd ~/ersathi-backend || { echo "[ERROR] Cannot find project directory"; exit 1; }

echo "[INFO] Pulling latest code..."
git pull origin main || { echo "[ERROR] Git pull failed"; exit 1; }

echo "[INFO] Rebuilding containers..."
docker compose pull
docker compose up -d --build || { echo "[ERROR] Docker build failed"; exit 1; }

echo "[SUCCESS] Deployment complete."