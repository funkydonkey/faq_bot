#!/bin/bash

# Start all FAQ Bot applications (Gradio, Streamlit, and Config)

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Starting FAQ Bot - All Applications"
echo "===================================="
echo "Project root: $PROJECT_ROOT"
echo ""

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3.12 -m venv venv"
    exit 1
fi

# Activate virtual environment
source "$PROJECT_ROOT/venv/bin/activate"

# Check for .env file
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Please create .env with OPENAI_API_KEY"
fi

echo "Starting applications..."
echo ""

# Start Gradio app
echo "🚀 Starting Gradio chat (port 8080)..."
cd "$PROJECT_ROOT"
python run_app.py > logs/gradio.log 2>&1 &
GRADIO_PID=$!
echo "   PID: $GRADIO_PID"

# Wait a bit
sleep 2

# Start Streamlit app
echo "🚀 Starting Streamlit chat (port 8082)..."
python run_streamlit.py > logs/streamlit.log 2>&1 &
STREAMLIT_PID=$!
echo "   PID: $STREAMLIT_PID"

# Wait a bit
sleep 2

# Start Config app
echo "🚀 Starting Config GUI (port 8081)..."
python run_config.py > logs/config.log 2>&1 &
CONFIG_PID=$!
echo "   PID: $CONFIG_PID"

echo ""
echo "✅ All applications started!"
echo ""
echo "Access at:"
echo "  • Gradio:    http://localhost:8080"
echo "  • Streamlit: http://localhost:8082"
echo "  • Config:    http://localhost:8081"
echo ""
echo "To stop all applications:"
echo "  ./scripts/stop_all.sh"
echo ""
echo "PIDs saved to: $PROJECT_ROOT/pids.txt"

# Save PIDs to file
echo "$GRADIO_PID $STREAMLIT_PID $CONFIG_PID" > "$PROJECT_ROOT/pids.txt"
