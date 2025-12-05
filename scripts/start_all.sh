#!/bin/bash

echo "========================================"
echo "Person Detection System - Startup Script"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Check if MongoDB is running
echo "[1/4] Checking MongoDB..."
if pgrep -x mongod > /dev/null; then
    echo "MongoDB is already running."
else
    echo "Starting MongoDB..."
    sudo systemctl start mongodb
    sleep 2
fi
echo ""

# Start Backend API
echo "[2/4] Starting Backend API..."
cd "$PROJECT_DIR/backend-api"
npm start &
BACKEND_PID=$!
echo "Backend API started (PID: $BACKEND_PID)"
sleep 5
echo ""

# Start AI Module
echo "[3/4] Starting AI Module..."
cd "$PROJECT_DIR/ai-module"
python main.py &
AI_PID=$!
echo "AI Module started (PID: $AI_PID)"
sleep 3
echo ""

# Open Dashboard
echo "[4/4] Opening Dashboard..."
if command -v xdg-open > /dev/null; then
    xdg-open "$PROJECT_DIR/frontend/index.html"
elif command -v open > /dev/null; then
    open "$PROJECT_DIR/frontend/index.html"
else
    echo "Please open $PROJECT_DIR/frontend/index.html in your browser"
fi
echo ""

echo "========================================"
echo "System Started Successfully!"
echo "========================================"
echo ""
echo "Backend API: http://localhost:3000"
echo "Dashboard: Check your browser"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "AI Module PID: $AI_PID"
echo ""
echo "To stop the system, run: kill $BACKEND_PID $AI_PID"
echo ""
